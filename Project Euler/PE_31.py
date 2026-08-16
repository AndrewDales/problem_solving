from functools import lru_cache
import time

# Project Euler 31:
# Count the number of ways to make exactly 200 pence using UK coin denominations:
# 1, 2, 5, 10, 20, 50, 100 and 200.
# We only care about combinations, not order, so each coin denomination is used
# in a constrained way: once we choose a denomination, we count the number of ways
# to make the remaining total with smaller denominations.

@lru_cache(maxsize=2000)
def coins(n, coin_list):
    # Base case: only one denomination remains.
    # If the remaining total is divisible by that coin, there is exactly one way
    # to form it using that coin alone (e.g. 50 -> 50p, 100 -> 100p, etc).
    # Otherwise, there are no valid combinations.
    if len(coin_list) == 1:
        if n % coin_list[0] == 0:
            num_partitions = 1
        else:
            num_partitions = 0
    else:
        # Use the largest remaining coin, then decide how many times it appears in
        # the combination. For each possible count i, recurse on the remaining
        # total with the smaller coin denominations.
        coin = coin_list[-1]
        remaining_coins = coin_list[:-1]
        num_partitions = sum(
            coins(n - coin * i, remaining_coins)
            for i in range(n // coin + 1)
        )
    return num_partitions


if __name__ == '__main__':
    # UK coins in pence, stored as a tuple so they remain hashable for lru_cache.
    uk_coins = (1, 2, 5, 10, 20, 50, 100, 200)

    # Start the timer before running the recursive counting function.
    start_time = time.time()
    num_parts = coins(200, uk_coins)
    end_time = time.time()

    # Print the number of combinations and the runtime for comparison/debugging.
    print(num_parts)
    print(f"Time taken: {end_time - start_time:,.6f} seconds")