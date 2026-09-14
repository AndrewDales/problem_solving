# Project Euler 76 - Counting Summations
# This uses exactly the same technique as Project Euler 31

from functools import lru_cache
import time

@lru_cache()
def summation(n:int, values = None)->int:
    if values is None:
        values = range(1, n)
    if n == 0:
        num_sums = 1
    elif n < 0 or not values:
        num_sums = 0
    else:
        max_value = max(values)
        num_sums = summation(n - max_value, range(1, min(max_value, n-max_value)+1)) + summation(n, range(1, max_value))
    return num_sums

if __name__ == "__main__":
    start_time = time.time()
    ways = summation(100)
    end_time = time.time()
    print(ways)
    print(f"Time taken: {end_time - start_time:,.6f} seconds")

