from redis import Redis
from redis.exceptions import ConnectionError
from os import getenv


"""Keys are used to identify data stored in Redis.
Example: If caching user information, you might use the user's ID as the key.
python
Copiar código
redis_client.set(f"user:{user_id}", json.dumps(user_data))"""


def str_to_bool(value: str) -> bool:
    """
        Transforms an string type to boolean.
    """
    return value.lower() in {"true", "1", "yes"}

try:
    redis_client = Redis(
        host=getenv("REDIS_HOST"),
        port=getenv("REDIS_PORT"),
        #password=getenv("REDIS_PASSWORD") or None, 
        ssl=str_to_bool(getenv("REDIS_SSL", "False")),
        socket_timeout=5
    )
    
    print("Connected to Redis!")
except Exception as e:
    print(f"Exception error: {e}")