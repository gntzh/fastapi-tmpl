import uuid

from dependency_injector.wiring import Provide
from sqlalchemy import Column, types

from src.libs.sa.timezone import TZDateTime
from src.libs.sa.uuid import UUID
from src.utils import utcnow

from .mapper import Base
from .services import PasswordHashService


class User(Base):
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(types.String, nullable=False, unique=True, index=True)
    password = Column(types.String, default=None)
    email = Column(types.String, default=None, unique=True, index=True)
    email_verified = Column(types.Boolean, default=False, nullable=False)
    is_active = Column(types.Boolean, default=True, nullable=False)
    date_joined = Column(TZDateTime, default=utcnow)
    is_superuser = Column(types.Boolean, default=False)

    password_hash_service: PasswordHashService = Provide["password_hash_service"]

    def set_password(self, raw_password: str):
        self.password = self.password_hash_service.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return self.password_hash_service.verify(raw_password, self.password)

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
