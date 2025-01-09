from src.models.user import User, Base, OneTimePassword, func, UserPreference


class UserManagementRepository:
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

    def get_user_by_email(self, email):
        session = self.Session()
        try:
            user = session.query(User).filter_by(email=email).first()
        finally:
            session.close()
        return user

    def get_user_by_id(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()
        return user

    def get_active_otp_by_user(self, user_id):
        session = self.Session()
        try:
            active_otps = (
                session.query(OneTimePassword)
                .filter_by(user_id=user_id, is_used=False)
                .filter(OneTimePassword.expires_at > func.now())
                .all()
            )
        finally:
            session.close()

        return active_otps

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
