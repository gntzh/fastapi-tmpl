from typing import Any

from fastapi import APIRouter, Depends

from src import schemas
from src.api import deps
from src.domain.user import User

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user
