from src.domain import Item, User  # noqa: F401
from src.domain.mapper import mapper_registry

__all__ = ["metadata"]

metadata = mapper_registry.metadata
