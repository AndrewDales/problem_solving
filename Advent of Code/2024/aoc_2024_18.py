from dataclasses import dataclass, field
from typing import Optional, Self
from queue import PriorityQueue
from collections import OrderedDict
import re
import heapdict

with open("data/aoc_input_2024_18.txt") as file:
    file_contents = file.read()

grid_size = 70
num_bytes = 1024

# file_contents = """5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0"""
#
# grid_size = 6
# num_bytes = 12

file_coordinates = re.findall(r'(\d+),(\d+)', file_contents)
file_coordinates = [(int(x), int(y)) for x, y in file_coordinates]


move_directions = {'W': (-1, 0), 'N': (0, -1), 'E': (1, 0), 'S': (0, 1)}


@dataclass
class Grid:
    walls: set[tuple[int, int]] = field(default_factory=set)
    end: tuple[int, int] = (0,0)
    start: tuple[int, int] = (0,0)
    n_rows: int = grid_size
    n_cols: int = grid_size

    def find_neighbours(self, pos):
        x, y = pos
        return ((x + x_d, y + y_d) for x_d, y_d in move_directions.values()
                if (0 <= x+x_d <= self.n_cols and
                    0 <= y+y_d <= self.n_rows and
                    not ((x + x_d, y + y_d) in self.walls)
                    )
                )

def find_path(memory_space:Grid):
    def find_path_cells(cell):
        opt_path = {cell}
        while cell != start:
            cell = visited[cell]
            opt_path.add(cell)
        return opt_path


    start = (0, 0)
    end = (grid_size, grid_size)

    current_node = start
    current_cost = 0

    visited = OrderedDict({start:0})
    priority_queue = heapdict.heapdict()

    while current_node != end:
        neighbour_nodes = memory_space.find_neighbours(current_node)
        for nn in neighbour_nodes:
            cost = current_cost + 1
            a_star_dist = cost + (end[0] - nn[0]) + (end[1] - nn[1])
            if nn not in visited:
                if nn not in priority_queue:
                    priority_queue[nn] = (a_star_dist, cost, current_node)
                else:
                    old_a_star_dist, *_ = priority_queue.get(nn)
                    if a_star_dist < old_a_star_dist:
                        priority_queue[nn] = (a_star_dist, cost, current_node)

        if not priority_queue:
            return None
        current_node, current_info  = priority_queue.popitem()
        _, current_cost, previous_node = current_info

        if current_node not in visited:
            visited[current_node] = previous_node

    return find_path_cells(end)

m_space = Grid(set(file_coordinates[:num_bytes]))
path = find_path(m_space)
paths = []

print(f'Solution to 18a is {len(path)-1}')

byte = (0,0)
for byte in file_coordinates[num_bytes:]:
    m_space.walls.add(byte)
    if byte in path:
        path = find_path(m_space)
        paths.append(path)
    if path is None:
        break

print(f'Solution to 18b is {byte[0]},{byte[1]}')