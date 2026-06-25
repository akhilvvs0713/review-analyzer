import redis
import json

import os
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0)

def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value: dict, expire_seconds: int = 60):
    redis_client.setex(key, expire_seconds, json.dumps(value))

def delete_cache(key: str):
    redis_client.delete(key)