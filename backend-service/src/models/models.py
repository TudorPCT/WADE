from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    activated = Column(Boolean, default=False)

    otps = relationship("OneTimePassword", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(email={self.email}, created_at={self.created_at}, activated={self.activated})>)>"


class OneTimePassword(Base):
    __tablename__ = "one_time_passwords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, default=text("(NOW() + INTERVAL '10 minutes')"))
    is_used = Column(Boolean, default=False)

    user = relationship("User", back_populates="otps")

    def __repr__(self):
        return f"<OneTimePassword(user_id={self.user_id}, otp={self.otp}, is_used={self.is_used})>"


class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preference_key = Column(String(255), nullable=False)
    preference_value = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, key={self.preference_key}, value={self.preference_value})>"

    def to_json(self):
        return {
            "id": self.id,
            "key": self.preference_key,
            "value": self.preference_value,
            "created_at": self.created_at,
        }