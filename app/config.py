from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    debug: bool = False
    origins: str = "localhost"
    database_url: str = "sqlite+aiosqlite:///db.sqlite3"
    redis_url: str = "memory://"
    ratelimit_enabled: bool = True
    ratelimit_guest: str = "6/minute"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings():
    return Settings()


# Instantiate settings for easy import elsewhere
settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis_url,
    strategy="moving-window",
    enabled=settings.ratelimit_enabled,
)
