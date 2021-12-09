from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.security import decode_access_token
from src.domain.user import User
from src.infra.repo.user import UserRepo

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@inject
async def get_current_user(
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    token: str = Depends(reusable_oauth2),
) -> User:
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    async with session.begin():
        user = await user_repo.get(payload.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
