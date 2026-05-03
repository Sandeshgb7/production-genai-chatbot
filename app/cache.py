import redis.asyncio as redis
from app.config import settings


# redis_client = redis.from_url(
#     settings.redis_url,
#     decode_responses=True
# )

import redis.asyncio as redis
from app.config import settings

_redis_client = None


def get_redis():
    global _redis_client

    if _redis_client is None:
        if not settings.redis_url:
            raise ValueError("REDIS_URL not set")

        _redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True
        )

    return _redis_client