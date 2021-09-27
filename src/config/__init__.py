from pathlib import Path

from pydantic import BaseSettings

BASE_DIR: Path = Path(__file__).resolve(strict=True).parent.parent.parent


class Settings(BaseSettings):
    BASE_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        case_sensitive = True
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
