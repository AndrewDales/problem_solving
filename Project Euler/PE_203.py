import math
from utilities import sieve_of_eratoshenes, factorise

last_row = 51
primes = sieve_of_eratoshenes(math.floor(math.sqrt(math.comb(last_row, last_row//2))))
print('Primes calculated')

bi_coeffs = set(math.comb(n, r)
                for n in range(1,last_row)
                for r in range(0, n//2 + 1))

square_free_combo = []

for bi_coeff in bi_coeffs:
    factors =  factorise(bi_coeff, primes)
    if len(factors) == len(set(factors)):
        square_free_combo.append(bi_coeff)

print(f'Solution to Project Euler 203 is {sum(square_free_combo)}')