import numpy as np
from collections import defaultdict

with open('data/aoc_input_2025_8_test.txt', 'r') as file:
    coords = [tuple(int(i) for i in line.strip().split(',')) for line in file]

def find_dist(x, y):
    d = np.array(x) - np.array(y)
    return np.sum(d * d)

distances = [[find_dist(coords[i], coords[j]), (coords[i], coords[j])]
             for i in range(len(coords))
             for j in range(i+1, len(coords))]

distances.sort()

groups = defaultdict(int)

group_number = 0
for _, coords in distances[:10]:
    c_1, c_2 = coords
    if not (c_1 in groups or c_2 in groups):
        groups[c_1] = group_number
        groups[c_2] = group_number
        group_number += 1
    elif c_1 in groups and c_2 in groups:
        if groups[c_1] != groups[c_2]:
            # combine groups
            ...