from src.models.models import User, Base, OneTimePassword, func, UserPreference


class PreferencesRepository:
    def __init__(self, Session):
        self.Session = Session

    def create(self, entity: Base):
        session = self.Session()
        try:
            session.add(entity)
            session.commit()
        finally:
            session.close()
        return entity

    def delete(self, entity: Base):
        session = self.Session()
        try:
            session.delete(entity)
            session.commit()
        finally:
            session.close()
        return entity

    def get_user_preference_by_id(self, preference_id, user_id):
        session = self.Session()
        try:
            preference = (
                session.query(UserPreference)
                .filter_by(id=preference_id, user_id=user_id)
                .first()
            )
        finally:
            session.close()
        return preference

    def get_user_preferences_by_key(self, key, user_id):
        session = self.Session()
        try:
            preferences = (
                session.query(UserPreference)
                .filter_by(user_id=user_id, preference_key=key)
                .all()
            )
        finally:
            session.close()
        return preferences

    def get_all_user_preferences(self, user_id):
        session = self.Session()
        try:
            preferences = (
                session.query(UserPreference)
                .filter_by(user_id=user_id)
                .all()
            )
        finally:
            session.close()
        return preferences
