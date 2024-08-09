import enum
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False
    environment: str = "DEV"
    log_level: LogLevel = LogLevel.INFO
    opentelemetry_endpoint: Optional[str] = None
    database_url: str = "postgresql+asyncpg://postgres:password@localhost/product_fusion"
    secret_key: str
    access_token_expire_minutes: int = 24 * 60
    jwt_algorithm: str = "HS256"
    refresh_token_expire_days: int = 30
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_username: str
    smtp_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def _settings() -> Settings:
    return Settings()  # type: ignore


settings: Settings = _settings()
