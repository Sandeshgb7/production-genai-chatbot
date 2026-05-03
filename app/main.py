from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import router
from app.core import setup_logging

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    # DO NOT connect DB/Redis in CI
    # Keep it lazy

    yield

    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)


app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}