import uuid

from jose import jwt

from src.domain import services
from src.infra import security

ALGORITHM = "HS256"
SIGNING_KEY = "secret"


def test_access_token_service():
    service = security.AccessTokenService(
        1, algorithm=ALGORITHM, signing_key=SIGNING_KEY
    )
    payload = services.TokenPayload(user_id=uuid.uuid4())
    token = service.create(payload)
    parsed_payload = jwt.decode(token, SIGNING_KEY, ALGORITHM)
    assert services.TokenPayload(**parsed_payload) == payload


def test_refresh_token_service():
    service = security.RefreshTokenService(
        1, algorithm=ALGORITHM, signing_key=SIGNING_KEY
    )
    payload = services.TokenPayload(user_id=uuid.uuid4())
    token = service.create(payload)
    parsed_payload = jwt.decode(token, SIGNING_KEY, ALGORITHM)
    assert services.TokenPayload(**parsed_payload) == payload


def test_recovery_token_service():
    service = security.RecoveryTokenService(
        1, algorithm=ALGORITHM, signing_key=SIGNING_KEY
    )
    payload = services.RecoveryTokenPayload(email="test@example.com")
    token = service.create(payload)
    parsed_payload = jwt.decode(token, SIGNING_KEY, ALGORITHM)
    assert services.RecoveryTokenPayload(**parsed_payload) == payload


def test_verify_email_token_service():
    service = security.VerifyEmailTokenService(
        1, algorithm=ALGORITHM, signing_key=SIGNING_KEY
    )
    payload = services.VerifyEmailTokenPayload(email="test@example.com")
    token = service.create(payload)
    parsed_payload = jwt.decode(token, SIGNING_KEY, ALGORITHM)
    assert services.RecoveryTokenPayload(**parsed_payload) == payload
