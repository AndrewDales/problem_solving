import math
from utilities_1 import sieve_of_eratoshenes

max_number = 10 ** 9
max_prime = 100

primes = sieve_of_eratoshenes(max_prime)

def hamming_numbers(max_n):
    if max_n == 1:
        h_nums = {1}
    else:
        h_nums = hamming_numbers(math.ceil(max_n / 2))
        h_nums |= {c for a in h_nums for b in primes
                if (c := a * b) <= max_n }
    return h_nums

hamming = hamming_numbers(max_number)
print(f'Solution to Project Euler 204 is {len(hamming)}')
