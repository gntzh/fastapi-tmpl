from uuid import UUID

from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRes(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class ChangePasswordData(BaseModel):
    old_password: str
    new_password: str


class RecoverPasswordData(BaseModel):
    email: EmailStr


class ResetPasswordData(BaseModel):
    token: str
    new_password: str


class VerifyEmailTokenReq(BaseModel):
    token: str


class TokenPayload(BaseModel):
    user_id: UUID


class RecoveryTokenPayload(BaseModel):
    email: EmailStr


class VerifyEmailTokenPayload(BaseModel):
    email: EmailStr
