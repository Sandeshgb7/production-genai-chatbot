from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

from app.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.postgres_url,
    echo=False,          # turn True only for debugging
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user / assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)




from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

engine = None
AsyncSessionLocal = None


def get_engine():
    global engine
    if engine is None:
        if not settings.postgres_url:
            raise ValueError("POSTGRES_URL not set")
        engine = create_async_engine(settings.postgres_url)
    return engine


def get_session():
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        AsyncSessionLocal = async_sessionmaker(get_engine(), expire_on_commit=False)
    return AsyncSessionLocal