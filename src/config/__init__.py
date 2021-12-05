from pathlib import Path
from typing import Any, Union

from pydantic import AnyHttpUrl, BaseSettings, root_validator, validator

BASE_DIR: Path = Path(__file__).resolve(strict=True).parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str
    BASE_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI: str
    CORS_ALLOWED_ORIGINS: list[AnyHttpUrl]

    JWT_ALGORITHM = "HS256"
    SIGNING_KEY: str
    VERIFYING_KEY: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    VERIFY_EMAIL_TOKEN_EXPIRE_MINUTES: int = 60
    RECOVERY_TOKEN_EXPIRE_MINUTES: int = 60

    VERIFY_EMAIL_CALLBACK_URL: Union[AnyHttpUrl, None] = None
    RECOVERY_CALLBACK_URL: Union[AnyHttpUrl, None] = None

    EMAIL_ENABLED: bool = False
    EMAIL_DEFAULT_FROM: Union[str, None] = None
    EMAIL_HOST: str = "localhost"
    EMAIL_PORT: Union[int, None] = None
    EMAIL_USERNAME: Union[str, None] = None
    EMAIL_PASSWORD: Union[str, None] = None
    EMAIL_USE_TLS: bool = False
    EMAIL_USE_STARTTLS: bool = False

    LOGGING_LEVEL: int = 20  # INFO

    @root_validator
    def check_smtp_tls_and_starttls(cls, values: dict[str, Any]):
        if values.get("EMAIL_USE_TLS") and values.get("EMAIL_USE_STARTTLS"):
            raise ValueError("The smtp starttls and tls options are not compatible")
        return values

    class Config:
        case_sensitive = True
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
