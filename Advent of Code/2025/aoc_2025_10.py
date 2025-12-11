import re
import numpy as np
import math

with open("data/aoc_input_2025_10_test.txt", 'r') as file:
    data = file.read()

lights = re.findall('\\[([#.]+)]', data)
buttons = re.findall('\\s([\\s(\\d,)]+)\\s', data)
jolts = re.findall('{([\\d,]+)}', data)

def pos_to_bin(positions, n):
    return sum(2 ** (n-i) for i in positions)

def buttons_to_numbers(button_str):
    button_list = re.findall('\\(([\\d,]+)\\)', button_str)
    button_tuples = [tuple(int(i) for i in  b_list.split(',')) for b_list in button_list]
    n_max = max(max(b_tuple) for b_tuple in button_tuples)
    return [pos_to_bin(b_tuple, n_max) for b_tuple in button_tuples]

def jolts_to_numbers(jolt_str):
    jolt_tuples = tuple(int(i) for i in jolt_str.split(','))
    jolt_val = 0
    for i in range(len(jolt_tuples)):
        jolt_val += jolt_tuples[-(i+1)] * 2**i
    return jolt_val

def num_to_bin_list(n, num_digits):
    b = []
    while n:
        b = [n  & 1] + b
        n >>= 1
    return [0] * (num_digits - len(b)) + b

def find_possible_light_vals(b_vals, combo_matrix):

    button_possible = np.matmul(combo_matrix, np.diag(b_vals))

    pos_vals = np.zeros(2**n, dtype=int)
    for i in range(n):
        pos_vals ^= button_possible[:, i]
    return pos_vals


light_vals = [int(light.replace('#','1').replace('.','0'), 2) for light in lights]
button_vals = [buttons_to_numbers(b_str) for b_str in buttons]
jolt_vals = [jolts_to_numbers(j_str) for j_str in jolts]

# max_digits = math.ceil(math.log(max(light_vals),2))
max_digits = max(len(bv) for bv in button_vals)

digit_matrix = np.array([num_to_bin_list(i, max_digits) for i in range(2**max_digits)])

num_presses = 0
for i in range(len(button_vals)):
    n = len(button_vals[i])
    combination_matrix = digit_matrix[:2 ** n, -n:]
    possible_light_vals = find_possible_light_vals(button_vals[i], combination_matrix)
    button_combos = combination_matrix[possible_light_vals==light_vals[i],:]
    num_presses += min(np.sum(button_combos, 1))

print(f'Solution to Day 10, part 1 is {num_presses}')