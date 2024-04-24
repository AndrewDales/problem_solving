MULTIPLES = range(2, 7)


def check_digit_permutation(n, m):
    return sorted(list(str(n))) == sorted(list(str(m)))


def num_check(n):
    multiples = [m * n for m in MULTIPLES]
    return tuple(check_digit_permutation(n, mult) for mult in multiples)


start_number = 100
found = False
trial = 0

while not found:
    trial = int(f'1{start_number}')
    found = all(num_check(trial))
    start_number += 1

print(f'Solution to Project Euler 52 is {trial}')
