from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from src import schemas
from src.api import deps
from src.domain import services
from src.domain.services import EmailService
from src.domain.user import User
from src.infra.repo.user import UserRepo

router = APIRouter()


@router.post("/register/", response_model=schemas.User)
@inject
async def register(
    data: schemas.Register,
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    email_service: EmailService = Depends(Provide["email_service"]),
    verify_email_token_service: services.VerifyEmailTokenService = Depends(
        Provide["verify_email_token_service"]
    ),
) -> Any:
    async with session.begin():
        if await user_repo.get_by_email(email=data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if await user_repo.get_by_username(username=data.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        user = User.register(**data.dict())
        session.add(user)
    await email_service.send_welcome_email(
        user.email,
        user.username,
        verify_email_token_service.create(
            services.VerifyEmailTokenPayload(email=data.email)
        ),
    )
    return user


@router.post("/token/", response_model=schemas.LoginRes)
@inject
async def token(
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    form_data: OAuth2PasswordRequestForm = Depends(),
    access_token_service: services.AccessTokenService = Depends(
        Provide["access_token_service"]
    ),
    refresh_token_service: services.RefreshTokenService = Depends(
        Provide["refresh_token_service"]
    ),
) -> Any:
    user = await user_repo.get_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": access_token_service.create(
            services.TokenPayload(user_id=user.id)
        ),
        "refresh_token": refresh_token_service.create(
            services.TokenPayload(user_id=user.id)
        ),
        "token_type": "bearer",
    }


@router.post("/token/refresh/")
@inject
async def refresh_token(
    refresh_token: str = Body(...),
    token_type: str = Body("bearer"),
    db: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    access_token_service: services.AccessTokenService = Depends(
        Provide["access_token_service"]
    ),
    refresh_token_service: services.RefreshTokenService = Depends(
        Provide["refresh_token_service"]
    ),
) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token_type.lower() != "bearer":
        raise credentials_exception
    try:
        payload = refresh_token_service.decode(refresh_token)
    except ValueError:
        raise credentials_exception

    async with db.begin():
        user = await user_repo.get(id=payload.user_id)
    if user is None:
        raise credentials_exception
    return {
        "token_type": "bearer",
        "access_token": access_token_service.create(
            services.TokenPayload(user_id=payload.user_id)
        ),
    }


@router.put("/password/")
@inject
async def change_password(
    data: schemas.ChangePasswordData,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(Provide["session"]),
) -> Any:
    if not current_user.verify_password(data.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )
    async with session.begin():
        current_user.set_password(data.new_password)
    return {"msg": "Password changed"}


@router.get("/emails/request-verification/")
@inject
async def send_verify_email(
    current_user: User = Depends(deps.get_current_user),
    email_service: EmailService = Depends(Provide["email_service"]),
    verify_email_token_service: services.VerifyEmailTokenService = Depends(
        Provide["verify_email_token_service"]
    ),
) -> Any:
    if current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )
    await email_service.send_verify_email(
        current_user.email,
        current_user.username,
        token=verify_email_token_service.create(
            services.VerifyEmailTokenPayload(email=current_user.email)
        ),
    )
    return {"msg": "Verification email sent"}


@router.post("/emails/confirm-verification/")
@inject
async def confirm_email_verification(
    data: schemas.VerifyEmailTokenReq,
    db: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    verify_email_token_service: services.VerifyEmailTokenService = Depends(
        Provide["verify_email_token_service"]
    ),
) -> Any:
    try:
        payload = verify_email_token_service.decode(data.token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    async with db.begin():
        user = await user_repo.get_by_email(payload.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
            )
        if user.email_verified:
            return {"msg": "Email already verified"}
        user.email_verified = True
    return {"msg": "Email verified"}


@router.post("/recovery/")
@inject
async def recover_account(
    data: schemas.RecoverPasswordData,
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    email_service: EmailService = Depends(Provide["email_service"]),
    recovery_token_service: services.RecoveryTokenService = Depends(
        Provide["recovery_token_service"]
    ),
) -> Any:
    user = await user_repo.get_by_email(email=data.email)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="That email address is not registered",
        )
    await email_service.send_recovery_email(
        user.email,
        token=recovery_token_service.create(
            services.RecoveryTokenPayload(email=data.email)
        ),
    )
    return {"msg": "Recovery email sent"}


@router.post("/password/reset/")
@inject
async def reset_password(
    data: schemas.ResetPasswordData,
    session: AsyncSession = Depends(Provide["session"]),
    user_repo: UserRepo = Depends(Provide["user_repo"]),
    recovery_token_service: services.RecoveryTokenService = Depends(
        Provide["recovery_token_service"]
    ),
) -> Any:
    try:
        payload = recovery_token_service.decode(data.token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    async with session.begin():
        user = await user_repo.get_by_email(email=payload.email)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="That email address is not registered",
            )
        user.set_password(data.new_password)
    return {"msg": "Password updated successfully"}
