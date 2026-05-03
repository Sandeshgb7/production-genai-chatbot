import redis.asyncio as redis
from app.config import settings

_redis_client: redis.Redis | None = None


def get_redis():
    global _redis_client

    if _redis_client is None:
        if not settings.redis_url:
            return None  # allow CI / no-redis mode

        _redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
        )

    return _redis_client


async def init_redis():
    client = get_redis()
    if not client:
        return

    try:
        await client.ping()
    except Exception:
        raise RuntimeError("Redis connection failed")