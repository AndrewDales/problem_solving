import time
# from PE_10 import prime_generator

def sieve_of_eratoshenes(max_prime=29):
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

if __name__  == "__main__":
    n = 10 ** 7
    tic = time.perf_counter()
    primes = sieve_of_eratoshenes(n)
    toc = time.perf_counter()
    print('Sieve', toc-tic)
