from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from src.config import settings
from src.schemas.auth import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    user_id: Any,
) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {
            "exp": expire,
            "user_id": str(user_id),
            "type": "access",
        },
        settings.SIGNING_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: Any) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {
            "exp": expire,
            "user_id": str(user_id),
            "type": "refresh",
        },
        settings.SIGNING_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def _decode_token(token: str, type: str = None) -> dict:
    try:
        claims = jwt.decode(
            token,
            settings.VERIFYING_KEY or settings.SIGNING_KEY,
            algorithms=settings.JWT_ALGORITHM,
        )
    except jwt.ExpiredSignatureError as e:
        raise ValueError("Expired token") from e
    except jwt.JWTError as e:
        raise ValueError("Invalid token") from e
    if type is not None:
        if claims.get("type") != type:
            raise ValueError("Invalid type")
    return claims


def decode_access_token(token: str) -> TokenPayload:
    try:
        return TokenPayload(**_decode_token(token, "access"))
    except ValidationError as e:
        raise ValueError("Invalid token") from e


def decode_refresh_token(token: str) -> TokenPayload:
    try:
        return TokenPayload(**_decode_token(token, "refresh"))
    except ValidationError as e:
        raise ValueError("Invalid token") from e
