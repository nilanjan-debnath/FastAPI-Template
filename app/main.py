from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.config import settings, limiter
from app.logger import logger, LoggingMiddleware
from app.db.core import create_session, DbSession
# from app.features.v1.controllers.routes import router as features_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # setup ratelimiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Rate limiter setup complete.")

    # Create the database session
    app.state.engine, app.state.Session = await create_session()
    logger.info("Database session setup complete.")

    # Yield control to the application
    yield

    # --- Shutdown ---
    logger.info("Shutting down...")
    await app.state.engine.dispose()
    logger.info("Database engine disposed.")


# Initialize the FastAPI app with the lifespan manager
app = FastAPI(
    title="FastAPI with Centralized Lifespan",
    docs_url=None if settings.env == "dev" else "/docs",
    redoc_url=None if settings.env == "dev" else "/redoc",
    openapi_url=None if settings.env == "dev" else "/openapi.json",
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


# app.add_route(features_v1_router)


@app.get("/")
async def root(request: Request):
    logger.info("logging message from root endpoint")
    return {"message": f"FastAPI is running on {settings.env} Environment"}


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
        # Log the error using the logger
        logger.error(f"Database connection failed: {str(e)}")
        return {"status": "error", "details": f"Database connection failed: {str(e)}"}
