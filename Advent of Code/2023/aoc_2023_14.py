import re
from dataclasses import dataclass

with open('data/aoc_input_2023_14.txt') as file:
    file_contents = file.read()


@dataclass
class Stone:
    row: int
    column: int
    symbol: str


@dataclass
class Dish:
    stones: list[Stone]
    n_rows: int
    n_columns: int

    def stone(self, i, j):
        if stone_list := [stone for stone in self.stones if stone.row == i and stone.column == j]:
            return stone_list[0]

    def row(self, n, min_col=0, max_col=None):
        if max_col is None:
            max_col = self.n_columns + 1
        return [stone for stone in self.stones if stone.row == n and min_col <= stone.column < max_col]

    def column(self, n, min_row=0, max_row=None):
        if max_row is None:
            max_row = self.n_rows + 1
        return [stone for stone in self.stones if stone.column == n and min_row <= stone.row < max_row]

    def move_line(self, row=None, col=None, direction=-1):
        if row is not None:
            stone_line = self.row(row)
            for stone in stone_line:
                if stone.symbol == 'O':
                    if direction == -1:
                        new_pos = max((stone.row for stone in self.column(stone.column, max_row=row)),
                                      default=-1) + 1
                        stone.row = new_pos
                    if direction == 1:
                        new_pos = min((stone.row for stone in self.column(stone.column, min_row=row+1)),
                                      default=self.n_rows) - 1
                        stone.row = new_pos

        if col is not None:
            stone_line = self.column(col)
            for stone in stone_line:
                if stone.symbol == 'O':
                    if direction == -1:
                        new_pos = max((stone.column for stone in self.row(stone.row, max_col=col)),
                                      default=-1) + 1
                        stone.column = new_pos
                    elif direction == 1:
                        new_pos = min((stone.column for stone in self.row(stone.row, min_col=col+1)),
                                      default=self.n_columns) - 1
                        stone.column = new_pos

    def tilt(self, direction):
        if direction == 'N':
            for i in range(1, self.n_rows):
                self.move_line(row=i, direction=-1)
        elif direction == 'S':
            for i in range(self.n_rows - 1, 0, -1):
                self.move_line(row=i-1, direction=1)
        elif direction == 'W':
            for i in range(1, self.n_columns):
                self.move_line(col=i, direction=-1)
        elif direction == 'E':
            for i in range(self.n_columns - 1, 0, -1):
                self.move_line(col=i-1, direction=1)

    def cycle(self):
        for d in 'NWSE':
            self.tilt(d)

    def calc_load(self):
        load = sum(sum(stone.symbol == 'O' for stone in self.row(i)) * (self.n_rows - i) for i in range(self.n_rows))
        return load

    def __str__(self):
        grid_string = ''
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if stone := self.stone(i, j):
                    grid_string += stone.symbol
                else:
                    grid_string += '.'
            grid_string += '\n'
        return grid_string


def parse_grid(grid_string):
    n_cols = grid_string.find('\n')
    grid_string = grid_string.replace('\n', '')
    n_rows = len(grid_string) // n_cols
    matches = re.finditer(r'[#|O]', grid_string)
    stones = [Stone(m.start() // n_cols, m.start() % n_cols, m.group(0)) for m in matches]
    return stones, n_rows, n_cols


dish = Dish(*parse_grid(file_contents))
dish.tilt('N')
print(f'Solution to Day 14, Problem 1 is {dish.calc_load()}')

dish = Dish(*parse_grid(file_contents))

load_n = 1000000000
dish_strings = {0: str(dish)}
dish_loads = {0: dish.calc_load()}
found_equal = False
count = 1
previous_dish = 0

while not found_equal:
    dish.cycle()
    dish_string = str(dish)

    print(count)

    if dish_string in dish_strings.values():
        previous_dish = [key for key, value in dish_strings.items() if value == dish_string][-1]
        found_equal = True
        dish_strings[count] = dish_string
        dish_loads[count] = dish.calc_load()
    else:
        dish_strings[count] = dish_string
        dish_loads[count] = dish.calc_load()
        count = count + 1


cycle_length = count - previous_dish
mod_position = (load_n - previous_dish) % cycle_length
load_position = previous_dish + mod_position

print(f'Solution to Day 14, Problem 2 is {dish_loads[load_position]}')
