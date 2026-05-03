from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

from app.config import settings

# =========================
# Base
# =========================

Base = declarative_base()

# =========================
# Model
# =========================

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# Lazy DB init (IMPORTANT)
# =========================

_engine = None
_SessionLocal = None


def get_engine():
    global _engine

    if _engine is None:
        if not settings.postgres_url:
            raise ValueError("POSTGRES_URL not set")

        _engine = create_async_engine(
            settings.postgres_url,
            echo=False,
            pool_pre_ping=True,
        )

    return _engine


def get_session():
    global _SessionLocal

    if _SessionLocal is None:
        _SessionLocal = async_sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
        )

    return _SessionLocal


# =========================
# Dependency (optional)
# =========================

async def get_db() -> AsyncSession:
    async with get_session()() as session:
        yield session