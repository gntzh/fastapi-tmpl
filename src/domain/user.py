import uuid

from sqlalchemy import Column, types

from src.infra.security import hash_password, verify_password
from src.libs.sa.timezone import TZDateTime
from src.libs.sa.uuid import UUID
from src.utils import utcnow

from .mapper import Base


class User(Base):
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(types.String, nullable=False, unique=True, index=True)
    password = Column(types.String, default=None)
    email = Column(types.String, default=None, unique=True, index=True)
    email_verified = Column(types.Boolean, default=False, nullable=False)
    is_active = Column(types.Boolean, default=True, nullable=False)
    date_joined = Column(TZDateTime, default=utcnow)
    is_superuser = Column(types.Boolean, default=False)

    def set_password(self, raw_password: str):
        self.password = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return verify_password(raw_password, self.password)

    @classmethod
    def _create_user(cls, username, email, password, **extra_fields) -> "User":
        user = cls(username=username, email=email, **extra_fields)
        user.set_password(password)
        return user

    @classmethod
    def register(cls, username: str, email: str, password: str) -> "User":
        return cls._create_user(username=username, email=email, password=password)

    @classmethod
    def create_superuser(cls, username: str, email: str, password: str) -> "User":
        return cls._create_user(
            username=username, email=email, password=password, is_superuser=True
        )
