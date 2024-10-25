#!/usr/bin/env python3
"""
This module defines a Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count in Redis for the qualified method name
        self._redis.incr(method.__qualname__)
        # Execute the original method
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Store the inputs and outputs in Redis lists
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, result)
        return result
    return wrapper


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

    @call_history
    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis and applies an optional conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Optional[Callable]): A callable to convert the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves a string from Redis by decoding it.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Optional[str]: The retrieved string data.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves an integer from Redis.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Optional[int]: The retrieved integer data.
        """
        return self.get(key, fn=int)


def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function.

    Args:
        method (Callable): The function to replay the history of.
    """
    redis = method.__self__._redis
    inputs = redis.lrange(f"{method.__qualname__}:inputs", 0, -1)
    outputs = redis.lrange(f"{method.__qualname__}:outputs", 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_.decode('utf-8')}) -> {output.decode('utf-8')}")


