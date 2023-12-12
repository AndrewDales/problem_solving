from collections import namedtuple
from itertools import combinations
import re

with open("data/aoc_input_2023_11.txt") as file:
    file_contents = file.read()

NUM_COLS = file_contents.find('\n')
NUM_ROWS = len(file_contents) // (NUM_COLS + 1)


def rc_is_empty(location_list, size=NUM_ROWS, dimension='row'):
    return [i for i in range(size) if not [loc for loc in location_list if getattr(loc, dimension) == i]]


def galaxy_expand(old_locations, expand=2):
    empty_rows = rc_is_empty(old_locations, NUM_ROWS, 'row')
    empty_cols = rc_is_empty(old_locations, NUM_COLS, 'column')
    return [Location(loc.row + sum(r < loc.row for r in empty_rows) * (expand-1),
                     loc.column + sum(c < loc.column for c in empty_cols) * (expand-1))
            for loc in old_locations]


file_contents = file_contents.replace('\n', '')
galaxy_search = re.finditer(r'#', file_contents)
Location = namedtuple('Location', 'row column')

galaxies = [Location(row=m.start() // NUM_COLS, column=m.start() % NUM_COLS) for m in galaxy_search]


distances = [abs(g1.row - g2.row) + abs(g1.column - g2.column) for
             g1, g2 in combinations(galaxy_expand(galaxies, 2), 2)]

print(f'Solution to Day 11, Problem 1 is {sum(distances)}')

expanded_distances = [abs(g1.row - g2.row) + abs(g1.column - g2.column) for
                      g1, g2 in combinations(galaxy_expand(galaxies, 1000000), 2)]

print(f'Solution to Day 11, Problem 2 is {sum(expanded_distances)}')
