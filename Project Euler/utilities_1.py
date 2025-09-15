""" Prime utility functions without numpy """

import time
from math import sqrt, floor
# from PE_10 import prime_generator

def sieve_of_eratosthenes(max_prime=29):
    prime_check = [True] * (max_prime+1)
    # Set 0 and 1 to not prime
    prime_check[0] = False
    prime_check[1] = False

    # Set all even numbers greater than 2 to not prime
    for i in range(4, max_prime + 1, 2):
        prime_check[i] = False

    # Loop through odd numbers
    p = 3
    while p * p < max_prime:
        # If p is prime mark all multiples of p equal or above p**2 to False
        if prime_check[p]:
            for i in range(p ** 2, max_prime + 1, p):
                prime_check[i] = False
        p += 2

    return [p for p in range(2, max_prime + 1) if prime_check[p]]

def digits_to_value(digit_array):
    if len(digit_array) == 1:
        val = digit_array[0]
    else:
        val = digit_array[-1] + 10 * digits_to_value(digit_array[:-1])
    return val

def factorise(n: int, prime_list=None):
    if prime_list is None:
        prime_list = sieve_of_eratosthenes(floor(sqrt(n)))
    if n in prime_list:
        prime_factors = [n]
    else:
        prime_factors = []
        prime_iter = iter(prime_list)
        p = next(prime_iter)

        while True:
            if n % p == 0:
                prime_factors.append(p)
                n = n // p
            else:
                try:
                    p = next(prime_iter)
                except StopIteration:
                    prime_factors.append(n)
                    break
            if p**2 > n:
                prime_factors.append(n)
                break
    return prime_factors





if __name__  == "__main__":
    n = 10 ** 7
    tic = time.perf_counter()
    primes = sieve_of_eratosthenes(n)
    toc = time.perf_counter()
    print(f'Time taken for primes up to {n:,} = {toc-tic:.3f} s')
    # n=10_000_000
    # p_factors = factorise(n)
    # print(n, p_factors)
