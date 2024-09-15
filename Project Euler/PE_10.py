def prime_generator(max_value = 2_000_000):
    primes = [2]
    trial = 3
    while trial <= max_value:
        for fac in primes:
            # not a prime
            if trial % fac == 0:
                break
            if fac ** 2 > trial:
                primes.append(trial)
                break
        trial +=2
        
    return primes

if __name__  == "__main__":
    n = 2_000_000
    prime_list = prime_generator(n)
    print(f'Sum of primes less than {n} is {sum(prime_list)}')