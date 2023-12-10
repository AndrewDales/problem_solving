from itertools import pairwise
import re

with open('data/aoc_input_2023_9.txt') as file:
    file_content = file.readlines()

lines = [re.findall(r'-?\d+', line) for line in file_content]
sequences = [[int(n) for n in line] for line in lines]


def calc_differences(seq):
    return [x[1] - x[0] for x in pairwise(seq)]


def find_next_value(seq):
    if all(x == 0 for x in seq):
        next_value = 0
    else:
        next_value = seq[-1] + find_next_value(calc_differences(seq))
    return next_value


print(f'Solution to Day 8, Problem 1 is {sum(find_next_value(sequence) for sequence in sequences)}')
print(f'Solution to Day 8, Problem 2 is {sum(find_next_value(sequence[::-1]) for sequence in sequences)}')
