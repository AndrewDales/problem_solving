import re
from collections import namedtuple, OrderedDict
from itertools import pairwise

with open("data/aoc_input_2023_18.txt") as file:
    file_contents = file.read()

DIRECTIONS = {'U': (-1, 0),
              'D': (1, 0),
              'R': (0, 1),
              'L': (0, -1),
              }
NUM_DIRECTIONS = {'0': 'R',
                  '1': 'D',
                  '2': 'L',
                  '3': 'U'
                  }

HLine = namedtuple('Line', 'row col_start col_end')
VLine = namedtuple('Line', 'col row_start row_end')

dig_data = re.findall(r"([LRUD]) (\d+) \(#(\w{6})\)", file_contents)
dig_commands = [(dd[0], int(dd[1])) for dd in dig_data]
dig_commands_big = [(NUM_DIRECTIONS[dd[2][-1]], int(dd[2][:-1], 16))
                    for dd in dig_data]


def find_edge():
    current_cell = (0, 0)
    edge = [current_cell]
    for command in dig_commands:
        direction = DIRECTIONS[command[0]]
        edge += [(current_cell[0] + i * direction[0],
                  current_cell[1] + i * direction[1])
                 for i in range(1, command[1] + 1)]
        current_cell = edge[-1]
    return set(edge)


def inside_range(location, row_limits, col_limits, margin=0):
    return (row_limits[0] + margin <= location[0] < row_limits[1] - margin
            and col_limits[0] + margin <= location[1] < col_limits[1] - margin)


def neighbours(location):
    return [(location[0] + direction[0], location[1] + direction[1]) for direction in DIRECTIONS.values()]


def move_location(location, direction, distance):
    dir_vec = DIRECTIONS[direction]
    return location[0] + distance * dir_vec[0], location[1] + distance * dir_vec[1]


def connected_group(location, edge_locations, row_limits, col_limits):
    group = set()
    adjacent = {location}

    while adjacent:
        current_cell = adjacent.pop()
        group.add(current_cell)
        new_neighbours = {ngh for ngh in neighbours(current_cell)
                          if (inside_range(ngh, row_limits, col_limits)
                              and ngh not in edge_locations
                              and ngh not in group
                              and ngh not in adjacent)
                          }
        adjacent |= new_neighbours
    return group


def find_inside_outside(edge_locs):
    inside_locs = set()
    outside_locs = set()
    row_range = (min(e[0] for e in edge_locs), max(e[0] + 1 for e in edge_locs))
    column_range = (min(e[1] for e in edge_locs), max(e[1] + 1 for e in edge_locs))

    unclassified = {(i, j) for i in range(*row_range) for j in range(*column_range) if (i, j) not in edge_locs}

    while unclassified:
        loc = unclassified.pop()
        loc_group = connected_group(loc, edge_locs, row_range, column_range)
        unclassified -= loc_group
        if all(inside_range(loc, row_range, column_range, 1) for loc in loc_group):
            inside_locs |= loc_group
        else:
            outside_locs |= loc_group

    return inside_locs, outside_locs


def find_lines(commands):
    h_lines = []
    v_lines = []
    current_loc = (0, 0)
    for cmd in commands:
        new_loc = move_location(current_loc, cmd[0], cmd[1])
        if cmd[0] == 'R':
            h_lines.append(HLine(row=current_loc[0], col_start=current_loc[1], col_end=new_loc[1]))
        elif cmd[0] == 'L':
            h_lines.append(HLine(row=current_loc[0], col_start=new_loc[1], col_end=current_loc[1]))
        if cmd[0] == 'D':
            v_lines.append(VLine(col=current_loc[1], row_start=current_loc[0], row_end=new_loc[0]))
        elif cmd[0] == 'U':
            v_lines.append(VLine(col=current_loc[1], row_start=new_loc[0], row_end=current_loc[0]))
        current_loc = new_loc
    return sorted(h_lines), sorted(v_lines)


def union_ranges(initial_ranges: list[tuple[int, int]]):
    initial_ranges.sort()
    new_ranges = [initial_ranges[0]]
    for current_range in initial_ranges[1:]:
        last_range = new_ranges.pop()
        if current_range[0] <= last_range[1] + 1:
            new_ranges.append((last_range[0], max(current_range[1], last_range[1])))
        else:
            new_ranges += [last_range, current_range]
    return new_ranges


def find_line_area(col, h_lines, v_lines):
    line_ranges = []

    h_lines = [h_line for h_line in h_lines if h_line.col_start <= col < h_line.col_end]
    v_lines = [v_line for v_line in v_lines if v_line.col == col]

    line_ranges += [(v_line.row_start, v_line.row_end) for v_line in v_lines]
    line_ranges += [(h_lines[i].row, h_lines[i + 1].row) for i in range(0, len(h_lines), 2)]

    line_ranges = union_ranges(line_ranges)

    return sum(line_range[1] - line_range[0] + 1 for line_range in line_ranges)


def find_area_from_lines(h_lines, v_lines):
    cols_with_lines = list(dict.fromkeys([line.col for line in v_lines]))
    area_lines = sum(find_line_area(col, h_lines, v_lines) for col in cols_with_lines)

    area = sum((col_end - col_start - 1) * find_line_area(col_start + 1, h_lines, v_lines)
               for col_start, col_end in pairwise(cols_with_lines)
               if col_end - col_start > 1)

    return area + area_lines


# edges = find_edge()
# rows = (min(e[0] for e in edges), max(e[0] + 1 for e in edges))
# columns = (min(e[1] for e in edges), max(e[1] + 1 for e in edges))
#
# insides, outsides = find_inside_outside(edges)
#
# with open('data/aoc_output_2023_18.txt', 'w') as file:
#     for i in range(*rows):
#         for j in range(*columns):
#             if (i,j) == (0, 0):
#                 file.write('S')
#             elif (i, j) in edges:
#                 file.write('#')
#             elif (i, j) in insides:
#                 file.write('I')
#             else:
#                 file.write('.')
#         file.write('\n')
#
# print(f'Solution to Day 1, part 1 is {len(edges) + len(insides)}')

horizontal_lines, vertical_lines = find_lines(dig_commands)

print(f'Solution to Day 1, part 1 is {find_area_from_lines(horizontal_lines, vertical_lines)}')

horizontal_lines_big, vertical_lines_big = find_lines(dig_commands_big)

print(f'Solution to Day 1, part 2 is {find_area_from_lines(horizontal_lines_big, vertical_lines_big)}')