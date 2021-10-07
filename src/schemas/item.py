from datetime import datetime
from typing import Union

from pydantic import BaseModel

from uuid import UUID

# TODO: fix Optional fields that are optional but can't be None.


class ItemBase(BaseModel):
    title: Union[str, None]
    description: Union[str, None]


class ItemCreate(ItemBase):
    title: str


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    id: int
    created_at: datetime
    title: str
    owner_id: UUID

    class Config:
        orm_mode = True


class Item(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass
