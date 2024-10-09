import numpy as np
import time

def prime_sieve(max_prime=1_000_000):
    prime_check = np.ones(max_prime+1, dtype=bool)
    # Set 0 and 1 to not prime
    prime_check[0] = False
    prime_check[1] = False

    # Set all even numbers greater than 2 to not prime
    prime_check[4::2] = False

    # Loop through odd numbers
    p = 3
    while p * p < max_prime:
        # If p is prime mark all multiples of p equal or above p**2 to False
        if prime_check[p]:
            prime_check[p**2::p] = False
        p += 2

    return np.nonzero(prime_check)[0]



if __name__ == "__main__":
    n = 1_000_000_000
    tic = time.perf_counter()
    primes = prime_sieve(n)
    toc = time.perf_counter()
    print(f'Time taken for primes up to {n:,} = {toc-tic:.3f} s')
