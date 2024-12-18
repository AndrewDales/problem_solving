from dataclasses import dataclass
import numpy as np
import re
from math import prod

with open('data/aoc_input_2024_14.txt') as file:
    file_contents = file.read()

width = 101
height = 103

# file_contents="""p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3"""
# width = 11
# height = 7

def find_quadrant(pos, w, h):
    quadrant = None
    if pos[0] < w // 2 and pos[1] < h // 2:
        quadrant = 0
    elif pos[0] < w // 2 and pos[1] > h // 2:
        quadrant = 1
    elif pos[0] > w // 2 and pos[1] < h // 2:
        quadrant = 2
    elif pos[0] > w // 2 and pos[1] > h // 2:
        quadrant = 3
    return quadrant

def draw_robots(pos_vec, w, h):
    print(f'time = {time}')
    for y in range(h):
        for x in range(w):
            count_rob = np.count_nonzero(np.all(np.array([x,y]) == pos_vec, axis=1))
            if count_rob:
                print(count_rob, end="")
            else:
                print('.',end='')
        print()

def find_position(pos, vel, t):
    pos_t = np.column_stack(((pos[:,0] + vel[:,0] * t) % width, (pos[:,1] + vel[:,1] * t) % height))
    return pos_t

position_values = re.findall(r'p=(\d+),(\d+)', file_contents)
velocity_values = re.findall(r'v=(-?\d+),(-?\d+)', file_contents)

position_vectors = np.array([np.array(p, dtype=int) for p in position_values])
velocity_vectors = np.array([np.array(p, dtype=int) for p in velocity_values])

# position_vector_100 = tuple(np.array([(p[0] + v[0] * 100) % width, (p[1] + v[1] * 100) % height])
#                             for p, v in zip(position_vectors, velocity_vectors))

position_vector_100 = find_position(position_vectors, velocity_vectors, 100)

quadrants = tuple(find_quadrant(vec, width, height) for vec in position_vector_100)
robot_count = prod(quadrants.count(i) for i in range(4))

print(f'Solution to Day 14a is {robot_count}')

time = 1
moving = True
while moving:
    position_vectors_t = find_position(position_vectors, velocity_vectors, time)
    if len(position_vectors_t) == len(np.unique(position_vectors_t, axis=0)):
        draw_robots(position_vectors_t, width, height)
        moving = False
    else:
        time += 1

print(f'Solution to Day 14b is {time}')

