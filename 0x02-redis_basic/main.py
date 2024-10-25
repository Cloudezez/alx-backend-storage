#!/usr/bin/env python3
""" Main file """

from exercise import Cache, replay

cache = Cache()

s1 = cache.store("first")
s2 = cache.store("second")
s3 = cache.store(42)

# Replay history of cache.store calls
replay(cache.store)

