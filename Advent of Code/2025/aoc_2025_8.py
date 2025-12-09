import numpy as np
from collections import Counter
import math

with open('data/aoc_input_2025_8.txt', 'r') as file:
    coords = [tuple(int(i) for i in line.strip().split(',')) for line in file]

def find_dist(x, y):
    d = np.array(x) - np.array(y)
    return np.sum(d * d)

distances = [[find_dist(coords[i], coords[j]), (coords[i], coords[j])]
             for i in range(len(coords))
             for j in range(i+1, len(coords))]
distances.sort()

groups = dict()
group_number = 0
counter = 0
group_count = 0
final_coords = ( )

for _, edge in distances:
    c_1, c_2 = edge
    # Neither c_1 nor c_2 in groups - give them both the new group_number
    if not (c_1 in groups or c_2 in groups):
        groups[c_1] = group_number
        groups[c_2] = group_number
        group_number += 1
    # Both c_1 and c_2 already in groups - combine the groups
    elif c_1 in groups and c_2 in groups:
        g_1, g_2 = groups[c_1], groups[c_2]
        # Only act if c_1 and c_2 are not already connected
        if groups[c_1] != groups[c_2]:
            # combine groups by putting all the elements in g_2 into g_1
            for c in groups:
                if groups[c] == g_2:
                    groups[c] = g_1
            # group_number += 1
    elif c_1 in groups and c_2 not in groups:
        groups[c_2] = groups[c_1]
    elif c_2 in groups and c_1 not in groups:
        groups[c_1] = groups[c_2]

    counter += 1
    if counter == 1000:
        group_counter = Counter(groups.values())
        group_count = sorted(list(group_counter.values()), reverse=True)

    if len(groups) == 1000 and len(set(groups.values())) == 1:
        final_coords = (c_1, c_2)
        break

print(f'Solution to Day 7, part 1 is {math.prod(group_count[:3])}')
print(f'Solution to Day 7, part 2 is {final_coords[0][0] * final_coords[1][0]} ')
