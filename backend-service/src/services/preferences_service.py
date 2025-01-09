import datetime
import secrets
import string

import bcrypt
import jwt

from src.models.user import UserPreference
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


class PreferencesService:

    def __init__(self, user_repository: UserManagementRepository):
        self.user_repository = user_repository

    def save_preference(self, user_id, key, value):
        user_preference = UserPreference(user_id=user_id, preference_key=key, preference_value=value)
        self.user_repository.create(user_preference)

    def delete_preference(self, preference_id, user_id):
        preference = self.user_repository.get_user_preference_by_id(preference_id, user_id)
        if preference:
            self.user_repository.delete(preference)

    def get_preferences_by_key(self, key, user_id):
        return self.user_repository.get_user_preferences_by_key(key, user_id)

    def get_all_preferences(self, user_id):
        return self.user_repository.get_all_user_preferences(user_id)
