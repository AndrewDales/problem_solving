from utilities import find_divisors_np
import numpy as np

abundant_numbers = np.fromiter((n for  n in range(1, 28123) if sum(find_divisors_np(n, True)) > n), dtype=int)
abundant_numbers_set = set(abundant_numbers)

not_abundant_sum = []
for trial in range(28123):
    remaining_number = trial - abundant_numbers[abundant_numbers < trial]
    if not set(remaining_number) & abundant_numbers_set:
        not_abundant_sum.append(trial)