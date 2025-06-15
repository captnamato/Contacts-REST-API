"""
Rate limiting для API endpoints
"""
import os
import redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import FastAPI, Request

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=0, decode_responses=True)
    redis_client.ping()
    storage_uri = f"redis://{REDIS_HOST}:{REDIS_PORT}"
except Exception:
    redis_client = None
    storage_uri = "memory://"

limiter = Limiter(key_func=get_remote_address, storage_uri=storage_uri)


def setup_rate_limiting(app: FastAPI):
    """Налаштування rate limiting для додатку"""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
