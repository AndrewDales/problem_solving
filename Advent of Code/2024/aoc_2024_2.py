from itertools import pairwise

with open("data/aoc_input_2024_2.txt") as file:
    file_contents = file.readlines()

def check_sequence(seq):
    diffs = [i - j for i,j in pairwise(seq)]
    diff_valid = []

sequences = []
for line in file_contents:
    sequences.append([int(val) for val in line.split(' ')])