from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from pydantic import ValidationError

from src.config import settings
from src.schemas.auth import RecoveryTokenPayload, TokenPayload, VerifyEmailTokenPayload


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


def create_recovery_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.RECOVERY_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {
            "exp": expire,
            "email": email,
            "type": "recovery",
        },
        settings.SIGNING_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_verify_email_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.VERIFY_EMAIL_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {
            "exp": expire,
            "email": email,
            "type": "verify_email",
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


def decode_recovery_token(token: str) -> RecoveryTokenPayload:
    try:
        return RecoveryTokenPayload(**_decode_token(token, "recovery"))
    except ValidationError as e:
        raise ValueError("Invalid token") from e


def decode_verify_email_token(token: str) -> VerifyEmailTokenPayload:
    try:
        return VerifyEmailTokenPayload(**_decode_token(token, "verify_email"))
    except ValidationError as e:
        raise ValueError("Invalid token") from e
