import sys

sys.path.insert(0, "")
import anyio  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

from src.domain.user import User  # noqa: E402
from src.infra.repo.user import UserRepo  # noqa: E402
from src.shared.container import Container  # noqa: E402


async def main():
    container = Container()
    container.wire()
    print(container.config.SQLALCHEMY_DATABASE_URI())
    session: AsyncSession = await container.session()
    user_repo: UserRepo = await container.user_repo()
    username = container.config.FIRST_SUPERUSER_USERNAME()
    email = container.config.FIRST_SUPERUSER_EMAIL()
    async with session.begin():
        user_in_db = await user_repo.get_by_username(username=username)
        print("dddddddddddd", user_in_db)
        if user_in_db is not None:
            return
        user_in_db = await user_repo.get_by_email(email=email)
        print("dddddddddddd", user_in_db)
        if user_in_db is not None:
            return
        user = User(
            username=username, email=email, is_superuser=True, email_verified=True
        )
        user.set_password(container.config.FIRST_SUPERUSER_PASSWORD())
        session.add(user)
    container.session.shutdown()


if __name__ == "__main__":
    anyio.run(main)
