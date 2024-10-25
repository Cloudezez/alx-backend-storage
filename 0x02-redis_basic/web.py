#!/usr/bin/env python3
"""
This module provides a function to retrieve and cache web pages
with an expiration time, while also tracking access counts.
"""

import requests
import redis
from typing import Callable

r = redis.Redis()


def count_access(fn: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.
    """
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        r.incr(f"count:{url}")
        return fn(url)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL, caching the response for 10 seconds.
    Counts the number of times each URL is accessed.

    Args:
        url (str): The URL to retrieve content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Check if the URL content is already cached
    cached_content = r.get(f"cache:{url}")
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch the page content if not cached
    response = requests.get(url)
    html_content = response.text

    # Cache the page content with a 10-second expiration
    r.setex(f"cache:{url}", 10, html_content)

    return html_content

