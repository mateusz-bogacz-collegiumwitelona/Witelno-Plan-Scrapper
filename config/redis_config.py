import json
import redis.asyncio as redis
from fastapi.encoders import jsonable_encoder

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

async def get_from_cache(key: str):
    data = await  client.get(key)
    if data:
        return json.loads(data)
    return None

async def save_to_cache(key: str, data, ttl: int = 3600):
    json_ready_data = jsonable_encoder(data)
    await client.set(key, json.dumps(json_ready_data), ex=ttl)

async def delete_from_cache(key: str):
    await client.delete(key)

