import numpy as np
from functools import lru_cache
import time

@lru_cache
def fib_mat_power(n):
    if n == 0:
        return np.array([[1, 1],[1,0]], dtype=object)
    else:
        return np.matmul(fib_mat_power(n-1), fib_mat_power(n-1))

def fib_exp(n):
    bin_n = f"{n:b}"
    fib_M = np.identity(2, dtype=object)
    for i, d in enumerate(bin_n[::-1]):
        if d == "1":
            fib_M = np.matmul(fib_M, fib_mat_power(i))
    return fib_M[1][0]

n = 2000000
tic = time.perf_counter()
f_n = fib_exp(n)
toc = time.perf_counter()
print(f"Found fib({n:,}) in {toc - tic:0.4f} seconds")
# print(f_n)
