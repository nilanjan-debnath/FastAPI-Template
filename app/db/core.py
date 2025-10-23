from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings


async def create_session():
    engine = create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

    Session = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine,
        class_=AsyncSession,
    )

    return engine, Session


async def get_session(request: Request):
    # Open a new session
    async with request.app.state.Session() as session:
        try:
            yield session
            # Commit the transaction if all went well
            await session.commit()
        except Exception:
            # Roll back in case of any error
            await session.rollback()
            raise
        finally:
            # The session is automatically closed by the 'async with' block
            pass


# Annotated dependency for easy type hinting in endpoints
DbSession = Annotated[AsyncSession, Depends(get_session)]
