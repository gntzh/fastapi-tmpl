from datetime import datetime, timedelta
from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from jose import jwt
from pydantic import BaseModel, ValidationError

from src.domain import services

payload_T = TypeVar("payload_T", bound=BaseModel)


class TokenServiceBase(Generic[payload_T]):
    token_type: str | None = None
    payload_model: Type[payload_T]

    def __init__(
        self,
        expire_minutes: int,
        algorithm: str,
        signing_key: str,
        verifying_key: str = None,
    ) -> None:
        self.expire_minutes = expire_minutes
        self.signing_key = signing_key
        self.algorithm = algorithm
        self.verifying_key = verifying_key

    def create(self, payload: payload_T):
        claims = jsonable_encoder(payload)
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        claims["type"] = self.token_type
        claims["exp"] = expire
        return jwt.encode(claims, self.signing_key, algorithm=self.algorithm)

    def decode(self, token: str) -> payload_T:
        try:
            claims = jwt.decode(
                token,
                self.verifying_key or self.signing_key,
                algorithms=self.algorithm,
            )
        except jwt.ExpiredSignatureError as e:
            raise ValueError("Expired token") from e
        except jwt.JWTError as e:
            raise ValueError("Invalid token") from e
        if claims.get("type") != self.token_type:
            raise ValueError("Invalid type")
        try:
            payload = self.payload_model(**claims)
        except ValidationError as e:
            raise ValueError("Invalid token") from e
        return payload


class AccessTokenService(TokenServiceBase[services.TokenPayload]):
    token_type = "access"
    payload_model = services.TokenPayload


class RefreshTokenService(TokenServiceBase[services.TokenPayload]):
    token_type = "refresh"
    payload_model = services.TokenPayload


class RecoveryTokenService(TokenServiceBase[services.RecoveryTokenPayload]):
    token_type = "recovery"
    payload_model = services.RecoveryTokenPayload


class VerifyEmailTokenService(TokenServiceBase[services.VerifyEmailTokenPayload]):
    token_type = "verify_email"
    payload_model = services.VerifyEmailTokenPayload
