# app/middleware.py

import time
from fastapi import Request

async def metrics_middleware(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    latency = time.time() - start

    print(f"latency={latency:.3f}s")

    return response