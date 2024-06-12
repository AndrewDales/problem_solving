import math


def is_pentagonal(p):
    return math.sqrt(1 + 24 * p) % 6 == 5


n = 1
pent_numbers = set()
pent_pair_found = False
new_pent_number: int = 0
other_pent_number: int = 0

while not pent_pair_found:
    new_pent_number = n * (3 * n - 1) // 2
    for other_pent_number in pent_numbers:
        sum_p = new_pent_number + other_pent_number
        if is_pentagonal(sum_p) and new_pent_number - other_pent_number in pent_numbers:
            print(new_pent_number, other_pent_number, new_pent_number - other_pent_number)
            pent_pair_found = True
            break

    pent_numbers.add(new_pent_number)
    n += 1

print(f'Solution to Project Euler 44 is {new_pent_number - other_pent_number}')
