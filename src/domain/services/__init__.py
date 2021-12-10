from typing import Protocol, TypeVar
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PasswordHashService(Protocol):
    def hash(self, password: str) -> str:
        ...

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        ...


class EmailService(Protocol):
    async def send_welcome_email(self, email: str, name: str, token: str) -> None:
        ...

    async def send_verify_email(self, email: str, name: str, token: str) -> None:
        ...

    async def send_recovery_email(self, email: str, token: str) -> None:
        ...


class TokenPayload(BaseModel):
    user_id: UUID


class RecoveryTokenPayload(BaseModel):
    email: EmailStr


class VerifyEmailTokenPayload(BaseModel):
    email: EmailStr


T = TypeVar("T")


class _TokenServiceBase(Protocol[T]):
    def create(self, payload: T) -> str:
        ...

    def decode(self, token: str) -> T:
        ...


class AccessTokenService(_TokenServiceBase[TokenPayload]):
    pass


class RefreshTokenService(_TokenServiceBase[TokenPayload]):
    pass


class RecoveryTokenService(_TokenServiceBase[RecoveryTokenPayload]):
    pass


class VerifyEmailTokenService(_TokenServiceBase[VerifyEmailTokenPayload]):
    pass
