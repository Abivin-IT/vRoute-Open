# =============================================================
# vFinacc — Async SQLAlchemy Database Engine & Session
# GovernanceID: vfinacc.0.0-DB
# =============================================================
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def _build_engine():
    """Build engine lazily — allows tests to import Base/get_db without asyncpg."""
    url = os.environ.get("DATABASE_URL")
    if url:
        # Ensure async driver — docker-compose may pass postgresql:// but we need asyncpg
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        from app.config import settings
        url = settings.database_url
    return create_async_engine(url, echo=False, pool_size=5, max_overflow=5)


# Lazy singleton — created on first real use (not at import time)
_engine = None
_async_session = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = _build_engine()
    return _engine


def _get_session_factory():
    global _async_session
    if _async_session is None:
        _async_session = async_sessionmaker(_get_engine(), class_=AsyncSession, expire_on_commit=False)
    return _async_session


async def get_db() -> AsyncSession:  # type: ignore[misc]
    """FastAPI Depends — yields an async session, auto-commits or rolls back."""
    async with _get_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
