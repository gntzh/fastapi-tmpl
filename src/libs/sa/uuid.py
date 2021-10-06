import uuid
from typing import TYPE_CHECKING, Optional, Union

from sqlalchemy import dialects, types

if TYPE_CHECKING:
    from sqlalchemy.engine import Dialect


# Refer to
# https://docs.sqlalchemy.org/en/14/core/custom_types.html#backend-agnostic-guid-type
class UUID(types.TypeDecorator):
    impl = types.BINARY(16)
    cache_ok = True
    python_type = uuid.UUID

    def load_dialect_impl(self, dialect: "Dialect"):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(dialects.postgresql.UUID(as_uuid=True))
        elif dialect.name == "mssql":
            return dialect.type_descriptor(dialects.mssql.UNIQUEIDENTIFIER())
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(
        self, value: Optional[uuid.UUID], dialect: "Dialect"
    ) -> Union[None, str, bytes]:
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        elif dialect.name == "mssql":
            return str(value)
        else:
            return value.bytes

    def process_result_value(
        self, value: Union[None, uuid.UUID, str, bytes], dialect: "Dialect"
    ) -> Union[None, uuid.UUID]:
        if value is None:
            return value
        else:
            if isinstance(value, uuid.UUID):
                return value
            elif isinstance(value, bytes):
                return uuid.UUID(bytes=value)
            return uuid.UUID(value)
