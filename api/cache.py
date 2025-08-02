import json
import os
import redis

# Initialize Redis connection using environment variables
_redis = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True)

# Retrieve a JSON object from Redis by key
def redis_get_json(key: str):
    val = _redis.get(key)
    return json.loads(val) if val else None

# Store a JSON object in Redis with a TTL (time to live)
def redis_set_json(key: str, data, ttl: int):
    _redis.setex(key, ttl, json.dumps(data, default=str))

# Delete a specific key from Redis
def invalidate_stats(_db):
    _redis.delete("last_bp_by_patient")
