from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings

BASE_DIR: Path = Path(__file__).resolve(strict=True).parent.parent.parent


class Settings(BaseSettings):
    BASE_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI: str
    CORS_ALLOWED_ORIGINS: list[AnyHttpUrl]

    JWT_ALGORITHM = "HS256"
    SIGNING_KEY: str
    VERIFYING_KEY: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    class Config:
        case_sensitive = True
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
