import numpy as np
import heapq

with open("aoc_input_2021_16_trial.txt", "r") as file:
    cave_data = np.array([[int(el) for el in line.strip()] for line in file])