import numpy as np
import re

with open('data/aoc_input_2024_13.txt') as file:
    file_contents = file.read()

# file_contents = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
#
# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176
#
# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450
#
# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=1027"""

A_values = re.findall(r'A:\sX\+(\d+),\sY\+(\d+)', file_contents)
B_values = re.findall(r'B:\sX\+(\d+),\sY\+(\d+)', file_contents)
prize_values = re.findall(r'X=(\d+),\sY=(\d+)', file_contents)

button_matrices = tuple(np.array([[a[0], b[0]],[a[1], b[1]]], dtype=int)
                        for a, b in zip(A_values, B_values))
prize_vectors = tuple(np.array(p, dtype=int) for p in prize_values)
prize_vectors_extend = np.array(tuple(p + 10_000_000_000_000 for p in prize_vectors), dtype=np.int64)

def find_tokens(b_matrices, p_vectors):
    tokens = 0
    for M, P in zip(b_matrices, p_vectors):
        sol = np.linalg.solve(M, P)
        X = np.rint(sol).astype(int)
        if all(np.matmul(M, X) == P) and all(X >= 0):
            tokens += X[0] * 3 + X[1]
    return tokens

print(f'Solution to Day 13a is {find_tokens(button_matrices, prize_vectors)}')
print(f'Solution to Day 13b is {find_tokens(button_matrices, prize_vectors_extend)}')
