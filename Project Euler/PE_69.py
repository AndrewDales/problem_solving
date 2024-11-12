from utilities import euler_totient, prime_sieve
import  time

MAX_N = 1_000_000

max_quotient = 1
n_max = 1
prime_list = prime_sieve(MAX_N)

for n in range(2, MAX_N + 1):
    q = (n / euler_totient(n, prime_list))
    # print(n, q)
    if q > max_quotient:
        max_quotient = q
        n_max = n

print(f'Solution to Project Euler 69 is {n_max}')