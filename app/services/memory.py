import json

try:
    from app.cache import get_redis

    redis_client = get_redis()
    USE_REDIS = True
except Exception:
    USE_REDIS = False


# fallback in-memory store (per process)
_memory_store = {}

CHAT_TTL = 3600


async def get_history(user_id: str, session_id: str):
    key = f"{user_id}:{session_id}"

    if USE_REDIS:
        try:
            data = await redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception:
            pass

    return _memory_store.get(key, [])


async def save_message(user_id: str, session_id: str, message: dict):
    key = f"{user_id}:{session_id}"

    history = await get_history(user_id, session_id)
    history.append(message)

    if USE_REDIS:
        try:
            await redis_client.set(key, json.dumps(history), ex=CHAT_TTL)
            return
        except Exception:
            pass

    # fallback
    _memory_store[key] = history