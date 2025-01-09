import datetime
import secrets
import string

import bcrypt
import jwt
from flask_mail import Mail, Message

from src.models.user import OneTimePassword
from src.repositories.users_repository import UserManagementRepository

def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
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


class UserService:

    def __init__(self, app, user_repository: UserManagementRepository, secret_key):
        self.mail = Mail(app)
        self.default_email = app.config['MAIL_DEFAULT_SENDER']
        self.user_repository = user_repository
        self.secret_key = secret_key

    def generate_password(self, email):
        password = generate_password()

        user_id = self.user_repository.get_user_by_email(email).id

        otp = OneTimePassword(otp=hash_password(password), user_id=user_id)
        self.user_repository.create(otp)

        msg = Message(
            subject="One-time password",
            sender=self.default_email,
            recipients=['tcosmin.pasat@gmail.com'],
            body=f"Your one time password is: {password}"
        )
        self.mail.send(msg)

        return ""

    def verify_password(self, email, otp):
        user = self.user_repository.get_user_by_email(email)
        active_otps = self.user_repository.get_active_otp_by_user(user.id)

        for active_otp in active_otps:
            if verify_password(otp, active_otp.otp):
                active_otp.is_used = True
                self.user_repository.create(active_otp)

                user_payload = {"user_id": user.id, "email": user.email}
                token = generate_jwt(user_payload, self.secret_key)
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
