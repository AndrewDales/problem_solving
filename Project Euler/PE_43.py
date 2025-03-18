DIGITS = set('01234567898')
MULTIPLES = [17, 13, 11, 7, 5, 3, 2, 1]


def add_digit(current_list, multiple):
    new_list = [i + val for val in current_list
                for i in DIGITS - set(val)
                if int(i + val[:2]) % multiple == 0]
    return new_list


pan = [d1 + d2 for d1 in DIGITS for d2 in DIGITS if d1 != d2]
for mult in MULTIPLES:
    pan = add_digit(pan, mult)

print(f'Solution to Project Euler 43 is {sum(int(p) for p in pan)}')
