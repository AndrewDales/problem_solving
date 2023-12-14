import re
from collections import namedtuple

with open('data/aoc_input_2023_13.txt') as file:
    file_contents = file.read()

Block = namedtuple('Block', ['n_rows', 'n_columns', 'cells'])
Cell = namedtuple('Cell', 'row column')


def parse_block(block_string):
    n_cols = block_string.find('\n')
    block_string = block_string.replace('\n', '')
    n_rows = len(block_string) // n_cols
    matches = re.finditer(r'#', block_string)
    cells = {Cell(row=m.start() // n_cols, column=m.start() % n_cols) for m in matches}
    return Block(n_rows, n_cols, cells)


def reflect_number(number, mirror):
    return 2 * mirror - (number + 1)


def reflect_block(block: Block, mirror, dim=1):
    if dim == 1:
        n = block.n_columns
    else:
        n = block.n_rows
    cells_to_reflect = {cell for cell in block.cells if 2*mirror - n <= cell[dim] < mirror}
    reflected_cells = set()
    for cell in cells_to_reflect:
        if dim == 1:
            reflected_cell = Cell(row=cell.row, column=reflect_number(cell.column, mirror))
        else:
            reflected_cell = Cell(row=reflect_number(cell.row, mirror), column=cell.column)
        reflected_cells.add(reflected_cell)
    return reflected_cells


def find_mirror(block: Block, part=1) -> int:
    # Check for vertical mirror
    dim = 1
    n = block.n_columns
    for mirror in range(1, n):
        reflected_block = reflect_block(block, mirror, dim)
        target_cells = {cell for cell in block.cells if mirror <= cell[dim] < min(n, 2 * mirror)}
        if reflected_block == target_cells and part == 1:
            break
        if len(reflected_block.symmetric_difference(target_cells)) == 1 and part == 2:
            break

    # No vertical mirror found
    # Check for horizontal mirror
    else:
        dim = 0
        n = block.n_rows
        for mirror in range(1, n):
            reflected_block = reflect_block(block, mirror, dim)
            target_cells = {cell for cell in block.cells if mirror <= cell[dim] < min(n, 2 * mirror)}
            if reflected_block == target_cells and part == 1:
                mirror *= 100
                break
            if len(reflected_block.symmetric_difference(target_cells)) == 1 and part == 2:
                mirror *= 100
                break
        else:
            mirror = None
    return mirror


block_strings = re.split(r'\n{2}', file_contents)
blocks = [parse_block(bs) for bs in block_strings]

mirrors = [find_mirror(block) for block in blocks]

print(f'Solution to Day 13, Problem 1 is {sum(mirrors)}')

# block = blocks[0]
#
# mirror = 3
# dim = 0
# r_block = reflect_block(block, 3, 0)
# target_cells = {cell for cell in block.cells if mirror <= cell[dim] < 2 * mirror}
mirrors_2 = [find_mirror(block, 2) for block in blocks]
print(f'Solution to Day 13, Problem 1 is {sum(mirrors_2)}')
