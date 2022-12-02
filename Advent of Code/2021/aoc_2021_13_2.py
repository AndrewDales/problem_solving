import numpy as np

def fold_pattern(coord_array, axis, value):
    if axis == 'x':
        col = 0
    else:
        col = 1
    coord_array[:,col] = value - abs(value - coord_array[:,col])
    coord_array = np.unique(coord_array, axis=0)
    return coord_array

with open("aoc_input_2021_13.txt", "r") as file:
    coords = []
    folds = []
    for line in file:
        if line[0].isdigit():
            coords.append([int(val) for val in line.strip().split(",")])
        elif line[0] == 'f':
            fold = line.replace('fold along ','').strip().split("=")
            fold[1] = int(fold[1])
            folds.append(fold)

coords = np.array(coords)
for fold in folds:
    coords = fold_pattern(coords, fold[0], fold[1])

n_row, n_col  = np.max(coords, axis=0)
pattern_grid = np.array([['.'] * (n_col + 1) for _ in range(n_row + 1)], 'str')
pattern_grid[tuple(coords.T)] = '#'

for row in pattern_grid.T:
    print("".join(row))