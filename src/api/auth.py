from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from src import schemas
from src.api import deps
from src.infra import security
from src.infra.repo.user import user_repo
from src.models.user import User

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def register(
    data: schemas.Register, session: AsyncSession = Depends(deps.get_db_session)
) -> Any:
    async with session.begin():
        if await user_repo.get_by_email(session, email=data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if await user_repo.get_by_username(session, username=data.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        user = User.register(**data.dict())
        session.add(user)
    return user


@router.post("/token", response_model=schemas.LoginRes)
async def token(
    db: AsyncSession = Depends(deps.get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = await user_repo.get_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/token/refresh")
async def refresh_token(
    refresh_token: str = Body(...),
    token_type: str = Body("bearer"),
    db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token_type.lower() != "bearer":
        raise credentials_exception
    try:
        payload = security.decode_refresh_token(refresh_token)
    except ValueError:
        raise credentials_exception

    async with db.begin():
        user = await user_repo.get(db, id=payload.user_id)
    if user is None:
        raise credentials_exception
    return {
        "token_type": "bearer",
        "access_token": security.create_access_token(payload.user_id),
    }
