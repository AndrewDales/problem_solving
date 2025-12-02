import math

import numpy as np
import time
from math import floor, sqrt , prod
from functools import lru_cache
from collections import Counter

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

def phi_sieve(n=100):
    # primes = prime_sieve(n)
    phi = np.arange(0, n + 1, dtype=int)
    #
    # for p in primes[primes <= n // 2]:
    #     phi[p*2::p] = phi[p*2::p] * (p-1) // p
    #
    # phi[1] = 0
    # phi[primes] -= 1
    # phi = phi[1:]


    phi[4::2] = phi[4::2] // 2
    m = 3

    while m * 2 <= n:
        # m is prime if the phi[m] == m-a
        if phi[m] == m:
            phi[m*2::m] = phi[m*2::m] * (m-1) // m
        m += 2

    phi = phi[1:]
    phi[phi == np.arange(1, n+1)] -= 1


    return phi



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

def prime_factorisation(n: int, prime_list=None):
    if prime_list is None:
        prime_list = prime_sieve(math.ceil(sqrt(n)))
    if n in prime_list or prime_list[0]**2 > n  or len(prime_list) == 0:
        prime_factors = [n]
    else:
        while (n % (p:= int(prime_list[0])) )!= 0 and p**2 < n:
            prime_list = prime_list[1:]
        prime_factors = [p] + prime_factorisation(n // p, prime_list)
    return prime_factors

def prime_factors_np(n: int, prime_list=None):
    if n == 1:
        return np.array([], dtype=int)
    if prime_list is None:
        prime_list = prime_sieve(math.ceil(sqrt(n)))
    else:
        prime_list = prime_list[prime_list <= n]
    prime_factors = prime_list[n % prime_list == 0]
    if len(prime_factors) == 0:
        return [n]
    else:
        return np.hstack((prime_factors, prime_factors_np(n // prod(prime_factors), prime_list)))

def find_divisors(n, prime_list=None):
    if prime_list is None:
        prime_list = prime_sieve(math.ceil(sqrt(n)))
    prime_factors = prime_factors_np(n, prime_list)
    prime_counter = Counter(prime_factors)
    divisors = [1]
    for p, num_p in prime_counter.items():
        divisors = [f * (p ** e) for f in divisors for e in range(num_p + 1)]
    return np.array(divisors)

def find_divisors_np(n):
    candidates = np.arange(1, n + 1, dtype=int)
    return candidates[n % candidates == 0]


def euler_totient(n: int, prime_list=None):
    """ Returns the Euler totient for n """
    if n == 1:
        return 0
    if prime_list is None:
        prime_list = prime_sieve(n // 2)
    p_factors = prime_list[n % prime_list == 0]

    return n * prod(p-1 for p in p_factors) // prod(p_factors)


def time_check(n=10_000_000):
    # With numpy
    tic = time.perf_counter()
    primes = prime_sieve(n)
    toc = time.perf_counter()
    print(f'Primes up to {n:,} calculated in {toc - tic:.3f}s - with numpy')

if __name__ == "__main__":
    max_n = 100_000_000
    time_check(max_n)
