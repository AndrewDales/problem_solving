from itertools import pairwise
import math

with open("data/aoc_input_2024_2.txt") as file:
    file_contents = file.readlines()


def check_sequence(seq):
    diffs = [i - j for i, j in pairwise(seq)]
    sign = math.copysign(1, diffs[0])
    diff_valid = [(math.copysign(1, d) == sign and 0 < abs(d) <= 3) for d in diffs]
    return all(diff_valid)


def check_sequence_2(seq):
    if check_sequence(seq):
        check = True
    else:
        check = any(check_sequence(seq[:i] + seq[i + 1:]) for i in range(len(seq)))
    return check


sequences = []
for line in file_contents:
    sequences.append([int(val) for val in line.split(' ')])

number_safe = sum(check_sequence(s) for s in sequences)
number_safe_2 = sum(check_sequence_2(s) for s in sequences)

print(f'Solution to Advent of Code 2024, problem 2a is {number_safe}')
print(f'Solution to Advent of Code 2024, problem 2b is {number_safe_2}')
