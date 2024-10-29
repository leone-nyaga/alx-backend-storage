import redis
import uuid
from typing import Union


class Cache:
    """A simple cache implementation using Redis."""

    def __init__(self) -> None:
        """Initialize the Cache and flush the Redis database.

        This method creates an instance of the Redis client and clears
        the existing data in the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the Redis cache.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in the cache.
        
        Returns:
            str: A unique key under which the data is stored in Redis.
        
        This method generates a random UUID key, stores the input data,
        and returns the key for future retrieval.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

