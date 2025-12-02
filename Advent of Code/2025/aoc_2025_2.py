# Read the file and format the ranges as numbers
with open('data/aoc_input_2025_2.txt', 'r') as file:
    file_contents = file.read()
    id_range = [ids.split('-') for ids in file_contents.split(',')]
    id_range_nums = [(int(id_val[0]), int(id_val[1])) for id_val in id_range]

def find_invalid_n(start, stop, n):
    """ Find values in range by repeating n digits """
    num_digits = len(str(start))
    if n <= 0 or n >= num_digits or num_digits % n != 0:
        return set()
    # Get the first n digits of start and end numbers
    start_part = start // (10 ** (num_digits - n))
    end_part = stop // (10 ** (num_digits - n))
    num_parts = num_digits // n

    # Create the repeated numbers by taking values from repeating the numbers from start_part to end_part, checking they
    # are in the correct range.
    invalid_ids = {val for i in range(start_part, end_part+1)
                   if start <= (val:=int(str(i) * num_parts)) <= stop
                   }
    return invalid_ids

def find_invalid_ids(start, stop, part=1) -> set[int]:
    n_start = len(str(start))
    n_stop = len(str(stop))
    # Deal recursively with different number of digits in start and end
    if n_start < n_stop:
        invalid_ids = find_invalid_ids(start, 10**n_start-1) | find_invalid_ids(10**n_start, stop)
    else:
        # In part 1, only look at repeating exactly half the digits in the start number
        if part == 1:
            invalid_ids = find_invalid_n(start, stop, n_start//2)
        else:
            # In part 2, we can repeat 1 up to half the digits in the start number (inclusive)
            invalid_ids = set()
            for i in range(1, n_start//2 + 1):
                invalid_ids = invalid_ids | find_invalid_n(start, stop, i)

    return invalid_ids

all_invalid_ids = set()
for id_range in id_range_nums:
    all_invalid_ids |= find_invalid_ids(id_range[0], id_range[1], 1)

print(f'Solution to AOC Day 2, part 1: {sum(all_invalid_ids)}')

all_invalid_ids = set()
for id_range in id_range_nums:
    all_invalid_ids |= find_invalid_ids(id_range[0], id_range[1], 2)

print(f'Solution to AOC Day 2, part 2: {sum(all_invalid_ids)}')