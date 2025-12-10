import numpy as np
from itertools import pairwise
from matplotlib import pyplot as plt

with open('data/aoc_input_2025_9.txt', 'r') as file:
    coords = [tuple(int(i) for i in line.strip().split(',')) for line in file]

def find_rect_size(coord_1, coord_2):
    return (abs(coord_1[0] - coord_2[0]) + 1) * (abs(coord_1[1] - coord_2[1]) + 1)

def find_lines(coord_list):
    # Add the first coord to the end to make a loop
    coord_list.append(coord_list[0])
    lines = set()
    for c_1, c_2 in pairwise(coord_list):
        # Vertical lines
        if c_1[0] == c_2[0]:
            y_min = min(c_1[1], c_2[1])
            y_max = max(c_1[1], c_2[1])
            line = (c_1[0], range(y_min, y_max + 1))
        # Horizontal lines
        elif c_1[1] == c_2[1]:
            x_min = min(c_1[0], c_2[0])
            x_max = max(c_1[0], c_2[0])
            line = (range(x_min, x_max + 1), c_1[1])
        else:
            print(f'Warning: {c_1}, {c_2} not on horizontal or vertical line')
            line = []
        lines.add(line)
    coord_list.pop()
    return lines

def check_inside(point):
    x, y = point
    lines_left = {v_line for v_line in v_lines
                if (v_line[0] <= x and y in v_line[1])}
    lines_below = {h_line for h_line in h_lines
                   if (x in h_line[0] and y <= h_line[1])}
    return len(lines_left) % 2 == 1 and len(lines_below) % 2 == 1

def check_range_intersection(a, b, c, d):
    return a < c < b or a < d < b or (c <= a and d >= b)

def check_line_inside(corner_points, line):
    a, b = corner_points
    x_min = min(a[0], b[0])
    x_max = max(a[0], b[0])
    y_min = min(a[1], b[1])
    y_max = max(a[1], b[1])
    # horizontal line
    if isinstance(line[0], range):
        return y_min < line[1] < y_max and check_range_intersection(x_min, x_max, min(line[0]), max(line[0]))
    else:
        return x_min < line[0] < x_max and check_range_intersection(y_min, y_max, min(line[1]), max(line[1]))

def check_all_lines(corner_points):
    return any(check_line_inside(corner_points, line) for line in all_lines)

rectangles = [(find_rect_size(coords[i], coords[j]), (coords[i], coords[j]))
             for i in range(len(coords))
             for j in range(i+1, len(coords))]

rectangles.sort(reverse=True)

print(f'Solution to Day 8, part 1 is {rectangles[0][0]}')

all_lines = find_lines(coords)
h_lines = {line for line in all_lines if isinstance(line[0], range)}
v_lines = {line for line in all_lines if isinstance(line[1], range)}
area = 0
corners = ((0, 0), (0, 0))

for rect in rectangles:
    area, corners = rect
    mid_point = ((corners[0][0] + corners[1][0]) // 2, (corners[0][1] + corners[1][1]) // 2)
    if not check_all_lines(corners) and check_inside(mid_point):
        break

print(f'Solution to Day 8, part 2 is {area}')

coords_np = np.array(coords)
plt.fill(coords_np[:,0], coords_np[:,1], edgecolor='red', fc=('green', 0.3))
r1, r2 = corners
plt.fill([r1[0], r1[0], r2[0], r2[0]], [r2[1], r1[1], r1[1], r2[1]], edgecolor='black', fc=('grey', 0.3))
plt.show()