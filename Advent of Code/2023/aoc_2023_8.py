import re
import math
from itertools import cycle

with open("data/aoc_input_2023_8.txt") as file:
    first_line = file.readline().strip()
    file_content = file.read()

directions = cycle(first_line)

matches = re.findall(r'([A-Z]{3}).*([A-Z]{3}).*([A-Z]{3})', file_content)
# matches = re.findall(r'([A-Z1-9]{3}).*([A-Z1-9]{3}).*([A-Z1-9]{3})', file_content)

map_dict = {match[0]: match[1:] for match in matches}


def find_path_length(start_loc, prob=1):

    current_loc = start_loc
    at_end = False
    count = 0

    while not at_end:
        count += 1
        direction = next(directions)
        if direction == 'L':
            current_loc = map_dict[current_loc][0]
        elif direction == 'R':
            current_loc = map_dict[current_loc][1]
        else:
            raise(ValueError("Can not read direction"))
        if current_loc == 'ZZZ' and prob == 1:
            at_end = True
        if current_loc[-1] == 'Z' and prob == 2:
            at_end = True
    return count


print(f'Solution to Day 8, Problem 1 is {find_path_length("AAA")}')

current_locations = [loc for loc in map_dict if loc[-1] == 'A']
counts = [find_path_length(loc, 2) for loc in current_locations]

print(f'Solution to Day 8, Problem 2 is {math.lcm(*counts)}')
