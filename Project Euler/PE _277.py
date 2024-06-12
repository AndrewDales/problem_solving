def reverse_collatz_step(a_out, step_type):
    if step_type == "D":
        a_in = a_out * 3
    elif step_type == "U":
        a_in = (a_out * 3 - 2) / 4
    elif step_type == "d":
        a_in = (a_out * 3 + 1) / 2
    else:
        a_in = None
    return a_in

def collatz_step(a_in):
    if a_in % 3 == 0:
        a_out, step_type = a_in // 3, "D"
    if a_in % 3 == 1:
        a_out, step_type = (4 * a_in + 2) // 3, "U"
    if a_in % 3 == 2:
        a_out, step_type = (2 * a_in - 1) // 3, "U"

def collatz_coefs(A, B, C, step_type):
    if step_type == "U":
        A = A * 4
        B = 4 * B + 2 * C
    if step_type == "d":
        A = A * 2
        B = 2 * B - C
    C = 3 * C
    return (A, B, C)

start_sequence = "UDDDUdddDDUDDddDdDddDDUDDdUUDd"
# start_sequence = ("UDDDUd")
#start_sequence = "DdDddUUdDD"
# min_input = 10**15
min_input = 10**6

A, B, C = 1, 0, 1
for symbol in start_sequence[:-1]:
    A, B, C = collatz_coefs(A, B, C, symbol)
    print(A, B, C)


# print(f'Solution to Project Euler 277 is {(n+1) * mod_base + a[-1]}')