from web import get_page
import time

# URL to test caching and access count
url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"

# First access - fetches from the web and caches the content
print("First access (should fetch from web):")
print

