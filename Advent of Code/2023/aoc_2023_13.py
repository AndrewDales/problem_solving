import re
from collections import namedtuple

with open('data/aoc_input_2023_13.txt') as file:
    file_contents = file.read()

Block = namedtuple('Block', ['n_rows', 'n_cols', 'cells'])
Cell = namedtuple('Cell', 'row column')


def parse_block(block_string):
    n_cols = block_string.find('\n')
    block_string = block_string.replace('\n', '')
    n_rows = len(block_string) // n_cols
    matches = re.finditer(r'#', block_string)
    cells = {Cell(row=m.start() // n_cols, column=m.start() % n_cols) for m in matches}
    return Block(n_rows, n_cols, cells)


block_strings = re.split(r'\n{2}', file_contents)
blocks = [parse_block(bs) for bs in block_strings]
