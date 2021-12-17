from email.message import EmailMessage
from typing import AsyncIterator

import pytest
from dependency_injector import providers
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.create_app import create_app
from src.domain import Item, User
from src.domain.mapper import Base
from src.domain.services import TokenPayload
from src.shared.container import Container
from tests.fakes.email import EmailSenderInMemory

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def container(anyio_backend) -> AsyncIterator[Container]:
    container = Container()
    container.config.from_pydantic(
        Settings(_env_file=container.config.BASE_DIR() / ".env.test")
    )
    container.email_sender.override(providers.Singleton(EmailSenderInMemory))
    print(container.email_sender())
    engine = container.db().engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print(container.email_service().email_sender)
    container.wire()
    yield container
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await container.db().dispose_db()


@pytest.fixture(scope="session")
def app(container: Container) -> FastAPI:
    return create_app(container)


@pytest.fixture(scope="session")
async def client(
    app: FastAPI,
):
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture(scope="session")
def email_outbox(container: Container) -> list[EmailMessage]:
    return container.email_sender().outbox  # type: ignore


@pytest.fixture(scope="session")
def config(container: Container) -> Settings:
    return container.config()


@pytest.fixture
async def session(container: Container):
    async with container.db().session() as session:
        yield session


@pytest.fixture(scope="session")
async def global_session(container: Container):
    async with container.db().session() as session:
        yield session


@pytest.fixture(scope="session")
async def test_user(global_session: AsyncSession) -> User:
    async with global_session.begin():
        user = User.register(
            username="test_user",
            email="test_user@example.com",
            password="test_user",
        )
        global_session.add(user)
    return user


@pytest.fixture(scope="session")
async def test_superuser(global_session: AsyncSession) -> User:
    async with global_session.begin():
        user = User.create_superuser(
            username="test_superuser",
            email="test_superuser@example.com",
            password="test_superuser",
        )
        global_session.add(user)
    return user


@pytest.fixture(scope="session")
def user_token_headers(test_user: User, container: Container) -> dict[str, str]:
    token = container.access_token_service().create(TokenPayload(user_id=test_user.id))
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def superuser_token_headers(
    test_superuser: User, container: Container
) -> dict[str, str]:
    token = container.access_token_service().create(
        TokenPayload(user_id=test_superuser.id)
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
async def test_item(global_session: AsyncSession, test_user):
    async with global_session.begin():
        item = Item(title="test_item", description="test_itm", owner=test_user)
        global_session.add(item)
    return item
