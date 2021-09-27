from src.models.mapper import mapper_registry
from src.models import User  # noqa: F401

__all__ = ["metadata"]

metadata = mapper_registry.metadata
