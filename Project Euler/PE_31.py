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


@lru_cache
def coin_partitions(target: int, coin_list: frozenset[int]):
    # Base case
    if target == 0:
        num_ways = 1
    elif target < 0 or not coin_list:
        num_ways = 0
    else:
        # Recursive relationship
        # Either the highest value coin is used, in which case reduce the target by its value
        # or the highest value coin is not used, in which case take it out of the coin_list
        high_coin = max(coin_list)
        num_ways = coin_partitions(target - high_coin, coin_list) + coin_partitions(target, coin_list - {high_coin})

    return num_ways

if __name__ == '__main__':
    # Number of ways to get 20p using only 1p and 2p
    print(coin_partitions(20, frozenset({1,2, 5})))

    # UK coins in pence, stored in a frozen set so they remain hashable for lru_cache.
    uk_coins = frozenset({1, 2, 5, 10, 20, 50, 100, 200})

    # Start the timer before running the recursive counting function.
    start_time = time.time()
    num_parts = coin_partitions(200, frozenset(uk_coins))
    end_time = time.time()

    # Print the number of combinations and the runtime for comparison/debugging.
    print(num_parts)
    print(f"Time taken: {end_time - start_time:,.6f} seconds")