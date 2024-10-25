Redis Caching Project
This project demonstrates caching, tracking, and counting web requests using Python and Redis. Through several tasks, we build a Cache class and additional utilities to cache data, track function call history, and cache web pages with expiration.


Requirements
Operating System: Ubuntu 18.04 LTS
Python Version: Python 3.7
Redis Version: Redis Server 5.x or higher
Python Packages:
redis (Install with pip3 install redis)
requests (For web.py, install with pip3 install requests)
Installation
Install Redis Server:

bash
sudo apt-get update
sudo apt-get -y install redis-server
sudo sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
sudo service redis-server start
Clone the Repository:

bash
Copy code
git clone https://github.com/cloudezez/alx-backend-storage.git
cd alx-backend-storage/0x02-redis_basic
Install Python Requirements:

bash
pip3 install -r requirements.txt
Tasks
Writing Strings to Redis
Create a Cache class with a store method to store strings, bytes, integers, or floats. The method generates a unique key for each value and stores it in Redis.

Reading and Recovering Original Types
The get method retrieves data from Redis and allows converting it to the original data type via an optional Callable argument, supporting str, bytes, int, or float formats.

Incrementing Function Calls
A count_calls decorator is used to count how many times specific functions in the Cache class are called. This uses the Redis INCR command to increment the call count.

Storing Function Call History
A call_history decorator tracks inputs and outputs of functions, storing them in separate lists in Redis (:inputs and :outputs keys).

Retrieving Call History
A replay function displays the history of function calls, showing each input and corresponding output in a structured format.

Expiring Web Cache
A get_page function caches web page content for a given URL, with an expiration of 10 seconds. It also tracks the number of times each URL is accessed.

Testing
Unit Tests
You can create unit tests using the provided main.py files and test_web.py script for each task. Running the tests requires an active Redis server.

bash
# Example: Running web cache test
python3 test_web.py
Authors
David - Initial work for ALX Backend Storage Project
