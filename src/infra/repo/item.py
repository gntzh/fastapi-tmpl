from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.libs.sa.uuid import UUID

from src.domain.item import Item

from .base import RepoBase


class ItemRepo(RepoBase[Item]):
    async def get_multi_by_owner(
        self, db: AsyncSession, /, owner_id: UUID, offset: int = 0, limit: int = 100
    ) -> list[Item]:
        return (
            (
                await db.execute(
                    select(self.model)
                    .where(Item.owner_id == owner_id)
                    .offset(offset)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )


item_repo = ItemRepo(Item)
