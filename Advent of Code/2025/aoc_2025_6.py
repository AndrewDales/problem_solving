import numpy as np
import re
from itertools import pairwise
from math import prod

operands = []
text_operands = []

with open("data/aoc_input_2025_6.txt", 'r') as file:
    for line in file:
        line = line.rstrip()
        if '+' not in line:
            strip_line = re.split('\\s+', line.lstrip())
            operands.append([int(val) for val in strip_line])
            text_operands.append(list(line))
        else:
            operators = re.split('\\s+', line)

def create_vals_from_word(word):
    return [int(s_word) for i in range(np.size(word, 1))
            if len(s_word := ''.join(word[:, i]).strip()) > 0]


operators = np.array(operators)
operands = np.array(operands)
text_operands = np.array(text_operands)

sums = np.sum(operands[:, operators=='+'], axis=0)
products = np.prod(operands[:, operators=='*'], axis=0)

print(f'Solution to Day 6, part 1 is {sum(sums) + sum(products)}')

split_points = np.flatnonzero(np.all(text_operands==' ', axis=0))
word_splits = [0,] + list(split_points) + [np.size(text_operands, 1),]
num_words = [text_operands[:,i:j] for i, j in pairwise(word_splits)]
word_vals = [create_vals_from_word(word) for word in num_words]

sums = (sum(vals) for vals, operator in zip(word_vals, operators) if operator == '+')
products = (prod(vals) for vals, operator in zip(word_vals, operators) if operator == '*')

print(f'Solution to Day 5, part 1 is {sum(sums) + sum(products)}')