def prime_generator(max_prime=10000):
    primes = [2]
    count = 3
    while count <= max_prime:
        for fac in primes:
            if count % fac == 0:
                break
            if fac ** 2 > count:
                primes.append(count)
                break
        count += 1
    return primes

def sprial_corners(prime_number_set):
    continue_spirals = True
    spiral_values = [1]
    spiral_primes = set()
    sprial_step = 2
    while continue_spirals:
        new_spiral_values = [spiral_values[-1] + i * sprial_step for i in range(1, 5)]
        new_spiral_primes = set(new_spiral_values) & prime_number_set
        spiral_values = spiral_values + new_spiral_values
        spiral_primes.update(new_spiral_primes)
        sprial_step += 2

        proportion_primes = len(spiral_primes) / len(spiral_values)
        
        print(proportion_primes)
        if proportion_primes < 0.4:
            continue_spirals = False
    print(spiral_values[-1])
    return sprial_step + 1

PRIMES = prime_generator(1_000)

print(sprial_corners(set(PRIMES)))