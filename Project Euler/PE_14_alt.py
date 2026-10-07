from functools import lru_cache
import time

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

@lru_cache(maxsize=None)
def collatz_chain_length(n):
    return 1 if n == 1 else collatz_chain_length(collatz_step(n)) + 1

tic = time.time()
_, long_start = max((collatz_chain_length(n),n) for n in range(1, 1_000_001))
print(f'Solution to Project Euler 13 {long_start}')
toc = time.time()

print(f'Time taken = {toc - tic:0.4f} seconds')