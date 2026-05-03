from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import router
from app.core import setup_logging


# setup logging early
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    # init connections here later (db, redis)
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)


# include routes
app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


#from app.cache import redis_client
from app.db import engine
from app.cache import get_redis

redis_client = get_redis()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    # DB check
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)

    # Redis check
    await redis_client.ping()

    logger.info("Connected to DB and Redis")

    yield

    logger.info("Shutting down application...")