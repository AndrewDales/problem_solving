import time
from utilities import prime_sieve, find_divisors_np

n = 10000
primes = prime_sieve(n)
prime_set = set(primes)

def check_divisors(n):
    divisors = find_divisors_np(n)
    mod_divisors = divisors + n // divisors
    return set(mod_divisors).issubset(prime_set)

# prime_generators = [(i, primes[i % primes == 0]) for i in range(1, 1000) if check_divisors(i)]
# print(prime_generators)

tic = time.perf_counter()
print(sum(i for i in range(2, n, 2) if check_divisors(i)))
toc = time.perf_counter()
print(toc - tic)