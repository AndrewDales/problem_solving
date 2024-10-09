from utilities import prime_sieve


def is_truncatable(p, prime_list):
    p_str = str(p)
    n_digits = len(p_str)
    truncatable = True
    for i in range(1, n_digits):
        # print(int(p_str[i:]))
        # print(p_str[:-i])
        if int(p_str[i:]) not in prime_list:
            truncatable = False
        if int(p_str[:-i]) not in prime_list:
            truncatable = False

    return truncatable

if __name__ == "__main__":
    primes = prime_sieve(1_000_000)
    truncatable_primes = [p for p in primes if is_truncatable(p, primes) and p > 10]
    print(f'Solution to Problem Euler 37 is {sum(truncatable_primes)}')
