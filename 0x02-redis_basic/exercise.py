#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps



def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        key = method.__qualname__

        self._redis.incr(key)
        
        return method(self, *args, **kwargs)

    return wrapper


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

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, int]]] = None) -> Optional[Union[str, int]]:
        """Retrieve data from the Redis cache and apply the conversion function if provided."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve data as a string from the cache."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve data as an integer from the cache."""
        return self.get(key, fn=lambda d: int(d))

