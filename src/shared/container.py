from typing import TYPE_CHECKING, AsyncIterator

from dependency_injector import containers, providers
from passlib.context import CryptContext

from src.config import Settings
from src.infra import email, security
from src.infra.database import Database
from src.infra.repo.item import ItemRepo
from src.infra.repo.user import UserRepo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker


async def session_resource(
    session_factory: "sessionmaker",
) -> AsyncIterator["AsyncSession"]:
    session: "AsyncSession" = session_factory()
    yield session
    await session.close()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src"], auto_wire=False)
    config = providers.Configuration(pydantic_settings=[Settings()])
    db = providers.Singleton(Database, config.SQLALCHEMY_DATABASE_URI)
    session = providers.Resource(session_resource, db.provided.session_factory)
    password_hash_service = providers.Singleton(
        CryptContext, schemes=["bcrypt"], deprecated=["auto"]
    )
    item_repo = providers.Factory(ItemRepo(), session.provided)
    user_repo = providers.Factory(UserRepo(), session.provided)
    email_sender = providers.Singleton(
        email.SMTPEmailSender,
        hostname=config.EMAIL_HOST,
        port=config.EMAIL_PORT,
        username=config.EMAIL_USERNAME,
        password=config.EMAIL_PASSWORD,
        use_tls=config.EMAIL_USE_TLS,
        start_tls=config.EMAIL_USE_STARTTLS,
    )
    email_service = providers.Singleton(email.EmailService, email_sender.provided)
    access_token_service = providers.Singleton(
        security.AccessTokenService,
        expire_minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        signing_key=config.SIGNING_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    refresh_token_service = providers.Singleton(
        security.RefreshTokenService,
        expire_minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES,
        signing_key=config.SIGNING_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    recovery_token_service = providers.Singleton(
        security.RecoveryTokenService,
        expire_minutes=config.RECOVERY_TOKEN_EXPIRE_MINUTES,
        signing_key=config.SIGNING_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    verify_email_token_service = providers.Singleton(
        security.VerifyEmailTokenService,
        expire_minutes=config.VERIFY_EMAIL_TOKEN_EXPIRE_MINUTES,
        signing_key=config.SIGNING_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
