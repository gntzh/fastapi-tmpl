import re
from datetime import datetime, timezone


def camel_to_snake(string: str) -> str:
    string = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", string).lower()


def utcnow() -> datetime:
    """Timezone Aware utcnow."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)
