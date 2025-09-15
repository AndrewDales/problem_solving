import math

import numpy as np
import time
from math import floor, sqrt , prod
from functools import lru_cache

def prime_sieve(max_prime=1_000_000):
    # Start by creating a list of 1s indicating (initially) that all numbers are prime
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

    # return the positions of all the values in prime_check that are not zero (in a 1d array)
    return np.flatnonzero(prime_check)


def factorise(n: int, prime_list=None):
    if prime_list is None:
        prime_list = prime_sieve(math.ceil(sqrt(n)))
    if n in prime_list:
        prime_factors = [n]
    else:
        prime_factors = []
        for p in prime_list:
            while n % p == 0:
                prime_factors.append(int(p))
                n = int(n // p)

            if p ** 2 > n:
                if n != 1:
                    prime_factors.append(n)
                break
    return prime_factors


def euler_totient(n: int, prime_list=None):
    """ Returns the Euler totient for n """
    if prime_list is None:
        prime_list = prime_sieve(n // 2)
    p_factors = set(factorise(n, prime_list))
    return n * prod(p-1 for p in p_factors) // prod(p_factors)


if __name__ == "__main__":
    max_p =100_000_000
    tic = time.perf_counter()
    primes = prime_sieve(max_p)
    toc = time.perf_counter()
    print(f'Time taken for primes up to {max_p:,} = {toc-tic:.3f} s')
