from utilities import prime_sieve, find_divisors

primes = prime_sieve(200_000_000)

def check_divisors(n):
    divisors = find_divisors(n, primes)
    mod_divisors = divisors + n // divisors
    return set(mod_divisors).issubset(primes)

# prime_generators = [i for i in range(1, 100) if check_divisors(i)]