from numpy.typing import NDArray
import numpy as np

ingredient_ranges = []
ingredient_ids = []

with open("data/aoc_input_2025_5.txt", 'r') as file:
    getting_ranges = True
    while getting_ranges:
        line = next(file)
        if '-' in line:
            line = line.strip().split('-')
            ingredient_ranges.append((int(line[0]), int(line[1])))
        else:
            getting_ranges = False
    next(file)
    ingredient_ids = [int(line.strip()) for line in file]

ingredient_ranges_np = np.array(ingredient_ranges)

def check_in_ranges(val, i_ranges) -> NDArray[np.bool_]:
    return (i_ranges[:,0] <= val) & (i_ranges[:,1] >= val)


print(f'Solution to Day 5, part 1 is {sum(any(check_in_ranges(ing_id, ingredient_ranges_np)) 
                                          for ing_id in ingredient_ids)}')

sorted_ranges = sorted(ingredient_ranges)

combined_ranges = []
c_range = sorted_ranges.pop(0)
combining_ranges = True

while combining_ranges:
    if not sorted_ranges:
        combined_ranges.append(c_range)
        combining_ranges = False
    else:
        next_range = sorted_ranges.pop(0)
        # ranges overlap
        if c_range[1] >= next_range[0]:
            c_range = (c_range[0], max(c_range[1], next_range[1]))
        else:
            combined_ranges.append(c_range)
            c_range = next_range

print(f'Solution to Day 5, part 1 is {sum((high - low + 1) for low, high in combined_ranges)}')