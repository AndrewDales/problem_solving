import math
import time
import numpy as np

from utilities import prime_sieve

n = 10**8
primes = prime_sieve(n//2)
print(f"{len(primes)} primes generated")

tic = time.perf_counter()
print(sum(np.sum((p<=primes) & (primes<=(n//p))) for p in primes[primes<math.ceil(math.sqrt(n))]))
toc = time.perf_counter()
print(toc-tic)