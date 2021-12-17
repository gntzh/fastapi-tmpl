from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.api import deps
from src.domain.user import User
from src.infra.repo.user import UserRepo

router = APIRouter()


@router.get("/me/", response_model=schemas.User)
async def me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user


@router.patch("/me/", response_model=schemas.User)
@inject
async def update_profile(
    data: schemas.UpdateProfileData,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(Provide["session"]),
) -> Any:
    async with session.begin():
        session.add(current_user)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(current_user, k, v)
            if k == "email":
                current_user.email_verified = False
        return current_user


@router.get("/", response_model=schemas.ListResult[schemas.User])
@inject
async def list_users(
    offset: int = 0,
    limit: int = 100,
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    superuser: User = Depends(deps.get_current_superuser),
) -> Any:
    return {
        "items": await user_repo.get_multi(offset, limit),
        "total_count": await user_repo.count(),
    }


@router.post("/", response_model=schemas.UserInDB)
@inject
async def create_user(
    data: schemas.UserCreate,
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    superuser: User = Depends(deps.get_current_superuser),
) -> Any:
    async with session.begin():
        if await user_repo.get_by_email(email=data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if await user_repo.get_by_username(username=data.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        user = User(**data.dict())
        user.set_password(data.password)
        session.add(user)


@router.get("/{id:uuid}/", response_model=schemas.UserInDB)
@inject
async def retrieve_user(
    id: UUID,
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    superuser: User = Depends(deps.get_current_superuser),
) -> Any:
    async with session.begin():
        item = await user_repo.get(id=id)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item


@router.patch("/{id:uuid}/", response_model=schemas.UserInDB)
@inject
async def update_user(
    id: UUID,
    data: schemas.UserUpdate,
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    session: AsyncSession = Depends(Provide["session"]),
    superuser: User = Depends(deps.get_current_superuser),
) -> Any:
    async with session.begin():
        user = await user_repo.get(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for k, v in data.dict(exclude_unset=True).items():
            if k == "password":
                user.set_password(v)
                continue
            setattr(user, k, v)
        return user


@router.post("/{id:uuid}/set-password/", response_model=schemas.User)
@inject
async def set_password(
    id: UUID,
    data: schemas.SetPasswordData,
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    session: AsyncSession = Depends(Provide["session"]),
    superuser: User = Depends(deps.get_current_superuser),
) -> Any:
    async with session.begin():
        user = await user_repo.get(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.set_password(data.password)
        return user


@router.delete(
    "/{id:uuid}/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
@inject
async def delete_user(
    id: UUID,
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    superuser: User = Depends(deps.get_current_superuser),
) -> None:
    async with session.begin():
        user = await user_repo.get(id=id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
