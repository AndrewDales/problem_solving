import time
import sys
from functools import lru_cache

sys.set_int_max_str_digits(1_000_000)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@lru_cache()
def fib_recursive(n):
    if n in (0, 1):
        return n
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


n = 1_000_000
tic = time.perf_counter()
for i in range(n):
    f_n = fib_recursive(i)
toc = time.perf_counter()
print(f"Found fib({n}) in {toc - tic:0.4f} seconds")
print(f_n)
