from math import floor, sqrt


def continued_fraction(n):
    recip_rem = floor(sqrt(n))
    a = [recip_rem]
    b = [recip_rem]
    c = [n - recip_rem ** 2]

    # stop if n is a square number (so c is 0)
    repeat_found = (c[0] == 0)

    while not repeat_found:
        a.append((recip_rem + b[-1]) // c[-1])
        b.append(a[-1] * c[-1] - b[-1])
        c.append((n - b[-1] ** 2) // c[-1])
        if b[-1] == b[0] and c[-1] == c[0]:
            repeat_found = True
        # print(a[-1],b[-1],c[-1])

    return a

if __name__ == '__main__':
    n = 10000
    continued_fractions = [continued_fraction(i) for i in range(n + 1)]
    odd_periods = sum(1 for a in continued_fractions if len(a) % 2 == 0)

    print(f"Number of continued fractions less than or equal to {n} with an odd period = {odd_periods}")