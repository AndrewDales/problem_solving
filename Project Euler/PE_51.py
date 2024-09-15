import numpy as np
from itertools import combinations, pairwise
from utilities import sieve_of_eratoshenes
import time


def find_max_replacement_primes(primes_np, choice_indices):
    num_digits = len(primes_np[0])
    choice_indices_p = list(set(range(num_digits)) - set(choice_indices))

    # Find all the primes with repeated digits in the chosen indices
    replacement_digits = primes_np[:, choice_indices]
    equal_indices = np.all(replacement_digits.T == replacement_digits[:, 0], axis=0)
    relevant_primes = primes_np[equal_indices,:]

    # Find all the unique patterns amongst the remaining digits and find which patter is the most frequent
    unique_patterns = np.unique(relevant_primes[:, choice_indices_p], return_inverse=True, return_counts=True, axis=0)
    max_patterns_loc = np.where(unique_patterns[2] == max(unique_patterns[2]))[0][0]
    return relevant_primes[(unique_patterns[1] == max_patterns_loc).flatten(), :]

def digits_to_value(digit_array):
    if len(digit_array) == 1:
        val = digit_array[0]
    else:
        val = digit_array[-1] + 10 * digits_to_value(digit_array[:-1])
    return val

tic = time.perf_counter()
primes = sieve_of_eratoshenes(1_000_000)

primes_5 = [p for p in primes if 10_000 <= p < 100_000]
primes_6 = [p for p in primes if 100_000 <= p < 1_000_000]
primes_array = np.array([[int(d) for d in str(p)] for p in primes_6])

n_digits = primes_array.shape[1]
prime_family = np.array([])
for r in range(1, n_digits-1):
    for c in combinations(range(n_digits), r):
        filtered = find_max_replacement_primes(primes_array, list(c))
        if len(filtered) > len(prime_family):
            prime_family = filtered

values = [digits_to_value(digits) for digits in prime_family]

print(f'Solution to Project Euler is {min(values)}')