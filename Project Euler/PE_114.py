""" Solution to Project Euler 114"""
from functools import lru_cache


@lru_cache
def block_combinations(n):
    if n <= 2:
        combos = 1
    elif n == 3:
        combos = 2
    else:
        combos = 2 * block_combinations(n - 1) + block_combinations(n - 4) - block_combinations(n - 2)
    return combos


num_ways = [block_combinations(i) for i in range(51)]
print(f'Solution to Project Euler 114 is {num_ways[-1]}')
