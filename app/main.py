from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.config import settings, setup_logger, LoggingMiddleware, limiter
from app.db.core import create_session, DbSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # setup logger
    app.state.logger = await setup_logger()
    app.state.logger.info("Logger setup complete.")

    # setup ratelimiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.state.logger.info("Rate limiter setup complete.")

    # Create the database session
    app.state.engine, app.state.Session = await create_session()
    app.state.logger.info("Database session setup complete.")

    # Yield control to the application
    yield

    # --- Shutdown ---
    app.state.logger.info("Shutting down...")
    await app.state.engine.dispose()
    app.state.logger.info("Database engine disposed.")


# Initialize the FastAPI app with the lifespan manager
app = FastAPI(
    title="FastAPI with Centralized Lifespan",
    docs_url=None if settings.production else "/docs",
    redoc_url=None if settings.production else "/redoc",
    openapi_url=None if settings.production else "/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins.split(" "),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add Logging middleware
app.add_middleware(LoggingMiddleware)


@app.get("/")
@limiter.limit(settings.ratelimit_guest)
async def root(request: Request):
    return {
        "message": f"FastAPI is running on {'Production' if settings.production else 'Development'} Environment"
    }


@app.get("/healthz")
@limiter.limit(settings.ratelimit_guest)
async def db_check(session: DbSession, request: Request):
    """
    Checks the database connection by executing a simple query.
    """
    try:
        _result = await session.execute(text("SELECT 1 + 1"))
        return {"status": "ok"}
    except Exception as e:
        # Log the error using the logger from app state
        request.app.state.logger.error(f"Database connection failed: {str(e)}")
        return {"status": "error", "details": f"Database connection failed: {str(e)}"}
