import numpy as np

with open("aoc_input_2021_7.txt", "r") as file:
    initial_state = file.readline()
    initial_state = np.array([int(i) for i in initial_state.strip().split(",")], int)

# For each position find the sum of the triangle numbers to move to that position
alignment_costs = [sum((d:= abs(initial_state-i)) * (d + 1) // 2) for i in range(max(initial_state))]

print(f'Output solution: {min(alignment_costs)}')