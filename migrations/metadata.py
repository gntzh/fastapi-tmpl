from src.models import Item, User  # noqa: F401
from src.models.mapper import mapper_registry

__all__ = ["metadata"]

metadata = mapper_registry.metadata
