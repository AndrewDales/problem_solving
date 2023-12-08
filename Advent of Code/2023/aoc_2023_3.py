import re

with open("data/aoc_input_2023_3.txt") as file:
    file_contents = file.read()


def parse_search(search_item):
    val = search_item.group()
    if val.isdigit():
        val = int(val)

    search_value = {'value': val,
                    'column': search_item.start() // num_cols,
                    'row_start': search_item.start() % num_cols,
                    'row_end': (search_item.end() - 1) % num_cols,
                    }
    return search_value


def check_adjacent(p_number: dict, p_symbol: dict) -> bool:
    """
    Checks whether a dictionary representing a number is next to a dictionary representing a symbol
    Parameters
    ----------
    p_number: number dictionary
    p_symbol: symbol dictionary

    Returns
    -------
    bool: True if the number and symbol are next to each other

    """
    col_check = abs(p_number['column'] - p_symbol['column']) <= 1
    row_check = (p_number['row_start'] <= (p_symbol['row_end'] + 1) and
                 p_number['row_end'] >= (p_symbol['row_start'] - 1))
    return col_check and row_check


def gear_value(p_symbol, p_numbers):
    gear_val = 0
    number_neighbours = [num for num in p_numbers if check_adjacent(num, p_symbol)]
    if len(number_neighbours) == 2:
        gear_val = number_neighbours[0]['value'] * number_neighbours[1]['value']
    return gear_val


num_cols = file_contents.find('\n')
file_contents = file_contents.replace('\n', '')

number_search = re.finditer(r'\d+', file_contents)
symbol_search = re.finditer(r'[^.\d]', file_contents)

numbers = [parse_search(ns) for ns in number_search]
symbols = [parse_search(ss) for ss in symbol_search]

adjacent_numbers = [num['value'] for num in numbers for sym in symbols if check_adjacent(num, sym)]

print(f'Solution to Day 3, problem 1 is {sum(adjacent_numbers)}')

gear_values = [gear_value(sym, numbers) for sym in symbols if sym['value'] == '*']

print(f'Solution to Day 3, problem 2 is {sum(gear_values)}')
