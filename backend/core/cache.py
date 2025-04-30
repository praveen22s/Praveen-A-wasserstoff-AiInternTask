import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Connect to Redis
cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def get_cached_verdict(key: str) -> dict | None:
    """Retrieve cached verdict and explanation."""
    raw = cache.get(key)
    print(f"🧩 Redis get for {key}: {raw}")  # Debug print
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"⚠️ JSON decode error for Redis value: {raw}")
        return None

async def set_cached_verdict(key: str, verdict: bool, explanation: str):
    """Cache both the verdict and its explanation."""
    data = {
        "verdict": verdict,
        "explanation": explanation
    }
    json_value = json.dumps(data)
    cache.setex(key, 3600, json_value)  # Cache for 1 hour
