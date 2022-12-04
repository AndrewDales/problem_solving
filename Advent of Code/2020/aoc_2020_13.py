import re

with open("aoc_2020_13.txt") as file:
    current_time = int(file.readline().strip())
    line_2 = file.readline()
    nums = re.findall(r'[0-9]+', line_2)
    buses = [int(num) for num in nums]

next_bus = {bus: bus - (current_time % bus) for bus in buses}

min_time_bus = [(k, v) for k, v in next_bus.items() if v == min(next_bus.values())]

print(f'Solution to part 1 is {min_time_bus[0][0] * min_time_bus[0][1]}')
