import numpy as np
from utilities import sieve_of_eratoshenes

primes = sieve_of_eratoshenes(10_000_000)

primes_4 = [p for p in primes if 1_000 <= p < 10_000]
primes_7 = [p for p in primes if 1_000_000 <= p < 10_000_000]
primes_array = np.array([[int(d) for d in str(p)] for p in primes_7])
num_digits = 7

primes_array_sorted = np.sort(primes_array, axis=1)
ii = (primes_array_sorted == list(range(1, num_digits+1))).all(axis=1)

highest_pos = max(np.where(ii)[0])

print(f'Solution of Project Euler 41 is {primes_7[highest_pos]}')