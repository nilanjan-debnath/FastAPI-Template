from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import sys
import time
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


async def setup_logger():
    # Remove any default handlers (avoid duplicate logs)
    logger.remove()

    # --- 1. Console Handler: simple human-readable output ---
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )

    # --- 2. File Handler: structured JSON logs ---
    logger.add(
        "logs/app.log",
        serialize=True,
        rotation="10 MB",  # or "00:00" for daily rotation
        retention="20 days",
        compression="zip",
        level="INFO",
        enqueue=True,
    )

    return logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Pre-request log
        request.app.state.logger.info(f"→ {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as e:
            # Log unhandled exceptions
            request.app.state.logger.exception(f"Unhandled error: {e}")
            raise
        finally:
            process_time = time.time() - start_time

            # Post-request log
            request.app.state.logger.info(
                f"← {request.method} {request.url.path} | "
                f"Status: {getattr(response, 'status_code', 'N/A')} | "
                f"{process_time:.4f}s"
            )

        return response
