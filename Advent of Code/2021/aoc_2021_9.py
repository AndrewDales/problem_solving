import numpy as np
from collections import deque

with open("aoc_input_2021_9.txt", "r") as file:
    data = []
    for line in file:
        line_list = list(line.strip())
        data.append([int(val) for val in line_list])

# Use breadth first search to find all the points connected with the min point, stopping at points with height 9
def breadth_first_area(point, data):
    visited = set()
    # Queue of points to visit
    point_queue = deque([point])
    # Posible directions of travel
    directions = (np.array((-1, 0)), np.array((1, 0)), np.array((0, -1)), np.array((0, 1)))
    n_row, n_col = data.shape
    
    # Continue until the point_queue is empty
    while point_queue:
        current_point = point_queue.popleft()
        visited.add(current_point)
        neighbours = [current_point + direction for direction in directions]
        neighbours = [tuple(point) for point in neighbours
                          if (all((0, 0) <= point ) and
                              all(point < (n_row, n_col)) and
                              not tuple(point) in visited) and
                              data[tuple(point)] < 9
                      ]
        point_queue.extend(neighbours)
    return visited
        
    
    

data = np.array(data, int)
n_row, n_col = data.shape

lt_above = np.vstack(([True] * n_col, data[1:,:] < data[:-1,:]))
lt_below = np.vstack((data[:-1,:] < data[1:, :], [True]* n_col))
lt_left = np.hstack((np.array([True] * n_row, ndmin=2).T, data[:, 1:] < data[:, :-1]))
lt_right = np.hstack((data[:, :-1] < data[:, 1:], np.array([True] * n_row, ndmin=2).T))

lt_all = lt_above & lt_below & lt_left & lt_right


print(f"Output solution, part 1 = {np.sum(lt_all * (data+1))}")

min_points = tuple(idx for idx, x in np.ndenumerate(lt_all) if x)

basins = sorted(len(breadth_first_area(point, data)) for point in min_points)

print(f"Output solution, part 2 = {np.prod(basins[-3:])}")
