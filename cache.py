import redis
import json

import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value: dict, expire_seconds: int = 60):
    redis_client.setex(key, expire_seconds, json.dumps(value))

def delete_cache(key: str):
    redis_client.delete(key)