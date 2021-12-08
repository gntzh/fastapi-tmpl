from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.repo.user import user_repo
from src.infra.security import decode_access_token
from src.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@inject
async def get_current_user(
    session: AsyncSession = Depends(Provide["session"]),
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
        user = await user_repo.get(session, payload.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
