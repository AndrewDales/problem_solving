# Project Euler 46 - 
import numpy as np

from utilities import prime_sieve


def goldbach_values(n, primes):
    primes = primes[primes < n ]
    goldbach_check = np.sqrt((n - primes) // 2) % 1 == 0
    return primes[goldbach_check]


PRIMES = prime_sieve(1_000_000)

i = 9
while True:
    if i not in PRIMES and not any(goldbach_values(i, PRIMES)):
        break
    i += 2

print(f'Solution to Project Euler 46 is {i}')