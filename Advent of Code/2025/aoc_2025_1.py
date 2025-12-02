import math

with open('data/aoc_input_2025_1.txt', 'r') as file:
    file_contents = file.read()

instructions = file_contents.split('\n')

count_zero = 0
count_pass_zero = 0
position = 50
for instruction in instructions:
    direction = instruction[0]
    distance = int(instruction[1:])
    if direction == 'L':
        start = position
        position -= distance
        if start > 0 >= position:
            count_pass_zero += 1
        if position < 0:
            count_pass_zero += (-position) // 100
    elif direction == 'R':
        position += distance
        if position >= 100:
            count_pass_zero += (position // 100)
    position = position % 100
    if position ==0:
        count_zero += 1

print(f'Solution for part 1: {count_zero}')
print(f'Solution for part 2: {count_pass_zero}')