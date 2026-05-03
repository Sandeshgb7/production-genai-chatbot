import asyncio
from app.db import  Base
from app.db import get_engine

engine = get_engine()
async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
#app\scripts\init_db.py