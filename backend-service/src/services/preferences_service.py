from src.models.user import UserPreference
from src.repositories.users_repository import UserManagementRepository


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
