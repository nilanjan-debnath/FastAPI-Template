from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    production: bool = True
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


async def setup_logger():
    # Configure logger
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("fastapi_app")
    return logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log before processing the request
        request.app.state.logger.info(
            f"Request started: {request.method} {request.url.path}"
        )

        response = await call_next(request)
        process_time = time.time() - start_time

        # Log after processing the request
        request.app.state.logger.info(
            f"Request finished: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Processing Time: {process_time:.4f}s"
        )
        return response
