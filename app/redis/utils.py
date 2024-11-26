from .connection import redis_client
from redis.exceptions import ResponseError
from fastapi import HTTPException

def save_hash(key: str, data: dict):
    try:
        sanitized_data = {str(k): str(v) for k, v in data.items()}
        redis_client.hset(name=key, mapping=sanitized_data)
    except ResponseError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")

def get_hash(key: str):
    try:
        raw_data = redis_client.hgetall(name=key)
        decoded_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_data.items()}
        # Convert fields to correct types if necessary
        if 'life_expectancy' in decoded_data:
            decoded_data['life_expectancy'] = int(decoded_data['life_expectancy'])
        return decoded_data
    except ResponseError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")
        
def delete_hash(key: str, keys: list):
    try:
        redis_client.hdel(key, *keys)
    except ResponseError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")