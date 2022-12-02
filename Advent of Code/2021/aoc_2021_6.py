from collections import Counter
import numpy as np
from numpy.linalg import matrix_power

with open("aoc_input_2021_6.txt", "r") as file:
    initial_state = file.readline()
    initial_state = [int(i) for i in initial_state.strip().split(",")]

NUM_STATES = 9

initial_state_count = Counter(initial_state)
pop_array = np.zeros(NUM_STATES, dtype=int)
for i, j in initial_state_count.items():
    pop_array[i] = j

transition_matrix = np.zeros((NUM_STATES, NUM_STATES), dtype = 'i8')

for i in range(1, NUM_STATES):
    transition_matrix[i-1, i] = 1

# A lanternfish in 0 mode becomes a 6-day fish and produces an 8-day fish
transition_matrix[6, 0] = 1
transition_matrix[8, 0] = 1

pop_80 = np.matmul(matrix_power(transition_matrix, 80), pop_array)
pop_256 = np.matmul(matrix_power(transition_matrix, 256), pop_array)

print(f'Output solution part 1: {sum(pop_80)}')
print(f'Output solution part 2: {sum(pop_256)}')