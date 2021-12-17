from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    date_joined: datetime
    is_superuser: bool
    email_verified: bool


class UserInDBBase(UserBase):
    id: Union[UUID, None] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str


class UpdateProfileData(BaseModel):
    username: Union[str, None] = None
    email: Union[EmailStr, None] = None


class UserUpdate(UpdateProfileData):
    email: Union[EmailStr, None] = None
    is_active: Union[bool, None] = None
    date_joined: Union[datetime, None] = None
    is_superuser: Union[bool, None] = None
    email_verified: Union[bool, None] = None
    password: Union[str, None] = None


class SetPasswordData(BaseModel):
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = False
    email_verified: bool = False
