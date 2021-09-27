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


class UserInDBBase(UserBase):
    id: Union[UUID, None] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
