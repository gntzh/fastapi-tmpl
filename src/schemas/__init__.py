from typing import Generic, TypeVar
from .auth import (  # noqa: F401
    ChangePasswordData,
    LoginRes,
    RecoverPasswordData,
    Register,
    ResetPasswordData,
    VerifyEmailTokenPayload,
    VerifyEmailTokenReq,
)
from .item import Item, ItemCreate, ItemUpdate  # noqa: F401
from .user import (  # noqa: F401
    SetPasswordData,
    UpdateProfileData,
    User,
    UserCreate,
    UserInDB,
    UserUpdate,
)
from pydantic.generics import GenericModel

T = TypeVar("T")


class ListResult(GenericModel, Generic[T]):
    items: list[T]
    total_count: int
