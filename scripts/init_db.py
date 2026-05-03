import asyncio
import logging

from app.db import Base, get_engine
from app.config import settings

logger = logging.getLogger("app")


async def init():
    if not settings.postgres_url:
        logger.warning("POSTGRES_URL not set, skipping DB init")
        return

    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created successfully")


if __name__ == "__main__":
    asyncio.run(init())