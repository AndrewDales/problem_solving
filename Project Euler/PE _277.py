# Use a recurrence relationship to find the coefficients
# (A * a_0 + B) / C = x mod 3, where a_o is the first value in the Collatz chain and each subsequent a_i in the
# sequence will satisfy the modulo requirement of the steps up to the last but one given in the DUd sequence.
# x is the value modulo 3 required by the last symbol in the DUd sequence

# This yield a modulo equation
# A * a_0 = C * (x - B) mod (3 * C)
# To solve this we need to use the extended Euclidean Algorithm to find A

# This gives a possible starting value for the DUd sequence - adding 3*C to this value will also yield a solution, so
# find the lowest value modulo 3*C which will exceed the min threshold for a_0

def collatz_coefs(A, B, C, step_type):
    if step_type == "U":
        A = A * 4
        B = 4 * B + 2 * C
    if step_type == "d":
        A = A * 2
        B = 2 * B - C
    C = 3 * C
    return (A, B, C)

def extended_euclidean(a, b):
    """ return (gcd, s, t) such that a * s + b * t = gcd(a, b)"""
    # if b == 0:
    #     (gcd, s_new, t_new) = (a, 1, 0)
    # else:
    #     q, r = divmod(a, b)
    #     a_new, b_new = q, r
    #     gcd, s_old, t_old = extended_euclidean(b, r)
    #     s_new = s_old - q
    # return gcd

    r = [a, b]
    s = [1, 0]
    t = [0, 1]

    while True:
        q, rem = divmod(r[-2], r[-1])
        if rem == 0:
            break
        r.append(rem)
        s.append(s[-2] - q * s[-1])
        t.append(t[-2] - q * t[-1])
    return s[-1], t[-1]


start_sequence = "UDDDUdddDDUDDddDdDddDDUDDdUUDd"
# start_sequence = "DdDddUUdDD"
min_input = 10**15
# min_input = 10**6

A, B, C = 1, 0, 1
for symbol in start_sequence[:-1]:
    A, B, C = collatz_coefs(A, B, C, symbol)
    print(A, B, C)

remainders = {'D': 0, 'U': 1, 'd': 2}
last_remainder = remainders[start_sequence[-1]]

A_inv = extended_euclidean(A, 3 * C)[0]
first_solution = A_inv * (C * last_remainder - B) % (3 * C)
smallest_possible_solution = ((min_input - first_solution) // (3 * C) + 1) * (3 * C) + first_solution
print(f'Solution to Project Euler 277 is {smallest_possible_solution}')