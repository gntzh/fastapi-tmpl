from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from src import schemas
from src.api.deps import get_db_session
from src.infra.repo.user import user_repo
from src.models.user import User

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def register(
    data: schemas.Register, session: AsyncSession = Depends(get_db_session)
) -> Any:
    async with session.begin():
        if await user_repo.get_by_email(session, email=data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if await user_repo.get_by_username(session, username=data.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        user = User.register(**data.dict())
        session.add(user)
    return user
