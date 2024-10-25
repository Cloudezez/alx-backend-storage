#!/usr/bin/env python3
"""
This module defines a Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class to interact with Redis for storing data.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance with a Redis client
        and flushes existing data in the Redis instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


