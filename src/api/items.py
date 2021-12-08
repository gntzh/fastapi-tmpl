from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.infra.repo.item import item_repo
from src.models.item import Item
from src.models.user import User

from . import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Item])
@inject
async def list_items(
    offset: int = 0,
    limit: int = 200,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(Provide["session"]),
) -> Any:
    print(current_user)
    if current_user.is_superuser:
        items = await item_repo.get_multi(session, offset, limit)
    else:
        items = await item_repo.get_multi_by_owner(
            session, current_user.id, offset, limit
        )
    return items


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
@inject
async def create_item(
    data: schemas.ItemCreate,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(Provide["session"]),
) -> Any:
    item = Item(**data.dict(), owner_id=current_user.id)
    async with session.begin():
        session.add(item)
    return item


@router.get("/{id:int}", response_model=schemas.Item)
@inject
async def retrieve_item(
    id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(Provide["session"]),
) -> Any:
    async with session.begin():
        item = await item_repo.get(session, id=id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if not current_user.is_superuser and (item.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        return item


@router.delete(
    "/{id:int}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
@inject
async def delete_item(
    id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(Provide["session"]),
) -> None:
    async with session.begin():
        item = await item_repo.get(session, id=id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if not current_user.is_superuser and (item.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        await session.delete(item)


@router.patch("/{id:int}", response_model=schemas.Item)
@inject
async def update_item(
    id: int,
    data: schemas.ItemUpdate,
    session: AsyncSession = Depends(Provide["session"]),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    async with session.begin():
        item = await item_repo.get(session, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if not current_user.is_superuser and (item.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        for k, v in data.dict(exclude_unset=True).items():
            setattr(item, k, v)
        return item
