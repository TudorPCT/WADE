from datetime import datetime, UTC, timedelta

from src.models.models import User, Base, OneTimePassword, func, UserPreference


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

    def get_unactivated_users(self):
        session = self.Session()
        try:
            one_week_ago = datetime.now(UTC) - timedelta(days=7)
            users = session.query(User).filter(
                User.activated == False,
                User.created_at < one_week_ago
            ).all()
        finally:
            session.close()
        return users
