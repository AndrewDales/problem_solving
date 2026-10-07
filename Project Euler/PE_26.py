from utilities import prime_sieve

def num_recurring_digits(n):
    nominator = 1
    count = 1
    while True:
        nominator = nominator * 10 % n
        if nominator == 0:
            return -1
        elif nominator == 1:
            return count
        else:
            count = count + 1

# Only need to consider primes, because 2*n has the same number of recurring digits as n
_, max_recurring_digits = max((num_recurring_digits(n), n) for n in prime_sieve(1000))
print(f'Solution to Project Euler 26 is {max_recurring_digits}')