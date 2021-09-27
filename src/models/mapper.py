from typing import Any

from sqlalchemy.orm import Mapped, declared_attr, registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

from src.utils import camel_to_snake

mapper_registry: registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor

    id: Mapped[Any]

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
