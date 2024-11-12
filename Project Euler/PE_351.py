import time

from utilities import euler_totient, prime_sieve
from time import perf_counter

tic = time.perf_counter()
MAX_N = 100_000
H = 0
prime_list = prime_sieve(MAX_N)

for i in range(2, MAX_N + 1):
    H += i - euler_totient(i, prime_list)

toc = time.perf_counter()
print(H * 6)
print(toc - tic)