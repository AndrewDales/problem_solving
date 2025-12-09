import numpy as np
from itertools import pairwise

from collections import Counter
import math

with open('data/aoc_input_2025_9_test.txt', 'r') as file:
    coords = [tuple(int(i) for i in line.strip().split(',')) for line in file]

def find_rect_size(coord_1, coord_2):
    return (abs(coord_1[0] - coord_2[0]) + 1) * ((abs(coord_1[1] - coord_2[1]) + 1))

def find_lines(coord_list):
    # Add the first coord to the end to make a loop
    coord_list.append(coord_list[0])
    h_lines = set()
    v_lines = set()
    for c_1, c_2 in pairwise(coord_list):
        # Veritical lines
        if c_1[0] == c_2[0]:
            y_min = min(c_1[1], c_2[1])
            y_max = max(c_1[1], c_2[1])
            line = (c_1[0], range(y_min, y_max + 1))
            v_lines.add(line)
        elif c_1[1] == c_2[1]:
            x_min = min(c_1[0], c_2[0])
            x_max = max(c_1[0], c_2[0])
            line = (range(x_min, x_max + 1), c_1[1])
            h_lines.add(line)
        else:
            print(f'Warning: {c_1}, {c_2} not on horizontal or vertical line')
    coord_list.pop()
    return h_lines, v_lines

def check_inside(point, lines):
    x, y = point
    h_lines, v_lines = lines
    lines_left = {v_line for v_line in v_lines
                if (v_line[0] <= x and y in v_line[1])}
    lines_below = {h_line for h_line in h_lines
                   if (x in h_line[0] and y <= h_line[1])}
    return len(lines_left) % 2 == 1 and len(lines_below) % 2 == 1

rectangles = [(find_rect_size(coords[i], coords[j]), (coords[i], coords[j]))
             for i in range(len(coords))
             for j in range(i+1, len(coords))]

def red_tile_inside(a, b, red_tile_coords):
    x_min, x_max = sorted((a[0], b[0]))
    y_min, y_max = sorted((a[1], b[1]))

    return any(x_min < x < x_max and y_min < y < y_max for x, y in red_tile_coords)

def check_inner_rect(a, b, lines):
    inside_point = ((a[0] + b[0])//2, (a[1] + b[1])//2)
    return check_inside(inside_point, lines)

rectangles.sort(reverse=True)

print(f'Solution to Day 8, part 1 is {rectangles[0][0]}')

all_lines = find_lines(coords)
area = 0

check_inside((5, 3), all_lines)

for rect in rectangles:
    area, corners = rect
    r1, r2 = corners
    if not red_tile_inside(r1, r2, coords) and check_inner_rect(r1, r2, all_lines):
        mid_x = (r1[0] + r2[0])//2
        mid_y = (r1[1] + r2[1])//2
        if (check_inside((mid_x, r1[1]), all_lines) and
                check_inside((mid_x, r2[1]), all_lines) and
                check_inside((r1[0], mid_y), all_lines) and
                check_inside((r2[0], mid_y), all_lines)):
            break


print(f'Solution to Day 8, part 1 is {area}')