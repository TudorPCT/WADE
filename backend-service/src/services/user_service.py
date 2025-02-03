import datetime
import os
import secrets
import string

import bcrypt
import jwt
from flask_mail import Mail, Message

from src.models.models import OneTimePassword, User
from src.repositories.users_repository import UserManagementRepository


def generate_password(length=10):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(plaintext.encode('utf-8'), hashed.encode('utf-8'))


def generate_jwt(payload, secret, algorithm="HS256", expiration_minutes=600):
    payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expiration_minutes)

    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


otp_subject_template = "Your OTP Code for WADE"
otp_email_template = """\
Hello {user_name},

Your one-time password (OTP) for WADE is: {otp_code}

This OTP is valid for the next {validity_period} minutes. Please use it to complete your action on {service_name}.

If you did not request this, please ignore this email or contact our support team at {support_email}.

Thank you,
WADE Team
"""


class UserService:

    def __init__(self, app, user_repository: UserManagementRepository, secret_key):
        self.mail = Mail(app)
        self.default_email = app.config['MAIL_DEFAULT_SENDER']
        self.user_repository = user_repository
        self.secret_key = secret_key

    def generate_password(self, email):
        code = 204
        content = ""

        password = generate_password()

        user = self.user_repository.get_user_by_email(email)

        if not user:
            user = User(email=email)
            self.user_repository.create(user)
            user = self.user_repository.get_user_by_email(email)
            code = 201

        active_otps = self.user_repository.get_active_otp_by_user(user.id)

        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)

        if len(active_otps) == 1 and active_otps[0].created_at > now - datetime.timedelta(minutes=1):
            code, content = 429, (active_otps[0].created_at + datetime.timedelta(minutes=1)).replace(
                tzinfo=datetime.UTC)
        elif len(active_otps) == 2 and active_otps[1].created_at > now - datetime.timedelta(minutes=3):
            code, content = 429, (active_otps[1].created_at + datetime.timedelta(minutes=3)).replace(
                tzinfo=datetime.UTC)
        elif len(active_otps) > 2 and active_otps[2].created_at > now - datetime.timedelta(minutes=5):
            code, content = 429, (active_otps[2].created_at + datetime.timedelta(minutes=5)).replace(
                tzinfo=datetime.UTC)
        else:
            otp = OneTimePassword(otp=hash_password(password), user_id=user.id)
            self.user_repository.create(otp)

            msg = Message(
                subject="One-time password",
                sender=self.default_email,
                recipients=[email],
                body=otp_email_template.format(
                    user_name=user.email,
                    otp_code=password,
                    validity_period=5,
                    service_name="WADE",
                    support_email=os.getenv('MAIL_USERNAME')
                )
            )
            self.mail.send(msg)

        return code, content

    def verify_password(self, email, otp):
        user = self.user_repository.get_user_by_email(email)
        active_otps = self.user_repository.get_active_otp_by_user(user.id)

        for active_otp in active_otps:
            if verify_password(otp, active_otp.otp):
                active_otp.is_used = True
                self.user_repository.create(active_otp)

                user_payload = {"user_id": user.id, "email": user.email}
                token = generate_jwt(user_payload, self.secret_key)

                if not user.activated:
                    user.activated = True
                    self.user_repository.create(user)

                return token

        return

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def delete_unactivated_users(self):
        users = self.user_repository.get_unactivated_users()
        for user in users:
            self.user_repository.delete(user)
