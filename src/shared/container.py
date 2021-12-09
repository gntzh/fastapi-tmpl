from typing import TYPE_CHECKING

from dependency_injector import containers, providers
from passlib.context import CryptContext

from src.config import Settings
from src.infra.database import Database
from src.infra.repo.item import ItemRepo
from src.infra.repo.user import UserRepo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker


async def session_resource(session_factory: "sessionmaker") -> "AsyncSession":
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
