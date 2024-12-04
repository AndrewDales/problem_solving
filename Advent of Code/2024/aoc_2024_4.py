import re
import numpy as np

test_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


with open('data/aoc_input_2024_4.txt') as file:
    file_contents = file.read()

# file_contents = test_data

def find_in_lines(word, letter_grid):
    string_list = [''.join(line) for line in letter_grid]
    forward_cases = sum(len(re.findall(word, line)) for line in string_list)
    backward_cases = sum(len(re.findall(word[::-1], line)) for line in string_list)
    return forward_cases + backward_cases

# Make the contents into lists
letters = [list(line.strip()) for line in file_contents.split('\n')]
n = len(letters)
# Find the transpose of the letters to search vertical
letters_t = [[row[i] for row in letters] for i in range(len(letters[0]))]
# Find the letters on the diagonal and off-diagonal of the letter grid
letters_d = [np.diag(letters, i) for i in range(-n + 1, n)]
letters_d_o = [np.diag(np.fliplr(letters), i) for i in range(-n + 1, n)]

count_h = find_in_lines('XMAS', letters)
count_v = find_in_lines('XMAS', letters_t)
count_d = find_in_lines('XMAS', letters_d)
count_d_o = find_in_lines('XMAS', letters_d_o)

print(f'Solution to Advent of Code 2024, problem 4a is {count_h + count_v + count_d + count_d_o}')

file_string = file_contents.replace('\n','')
find_a_iter = re.finditer('A', file_string)
xmas_count = 0

for match in find_a_iter:
    pos = match.span()[0]
    row, column = divmod(pos, n)
    if (0 < row < n - 1) and (0 < column < n - 1):
        surrounding_letters = ''.join([letters[row-1][column-1],
                                       letters[row-1][column+1],
                                       letters[row+1][column-1],
                                       letters[row+1][column+1],
                                      ])
        if surrounding_letters in {'MMSS', 'MSMS', 'SMSM', 'SSMM'}:
            xmas_count += 1

print(f'Solution to Advent of Code 2024, problem 4b is {xmas_count}')