import numpy as np

with open("data/aoc_input_2025_4.txt", 'r') as file:
    data: np.ndarray = np.array([list(line.strip()) for line in file])

data_bool: np.ndarray = data == '@'
num_rolls_start: int = int(np.count_nonzero(data_bool))

SHIFTS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]

def shift2d(arr: np.ndarray, dx: int = 0, dy: int = 0) -> np.ndarray:
    h, w = arr.shape
    top  = max(dy, 0)
    bottom = max(-dy, 0)
    left = max(dx, 0)
    right = max(-dx, 0)

    padded = np.pad(arr, ((top, bottom), (left, right)), mode='constant', constant_values=False)
    # Crop to original size, offsetting back
    return padded[bottom:bottom+h, right:right+w]

def remove_rolls(current_array: np.ndarray):
    """ Function works out the number of neighbours for each element in a boolean array and returns a boolean array
    which is True only for cells with 4 or more neighbours. Also return the count of the number of elements removed """

    # Count the number of neighbours by shifting the Boolean array in each of 8 directions and adding up
    # original AND shifted for each direction shift
    num_neighbours = sum(data_bool & shift2d(current_array, i, j) for i, j in SHIFTS)
    new_array = num_neighbours >= 4

    removed = current_array & ~new_array
    return new_array, np.count_nonzero(removed)



# Remove one set of paper rolls leaving only those which have 4 neighbours
data_bool, num_removed = remove_rolls(data_bool)

print(f'Solution to Day 4, part 1 is {num_removed}')

# Keep on removing rolls until there are no rolls with fewer than 4 neighbours
removing = True
while removing:
    data_bool, n = remove_rolls(data_bool)
    # print(n)
    if n == 0:
        removing = False

num_rolls_end = np.count_nonzero(data_bool)

print(f'Solution to Day 4, part 1 is {num_rolls_start - num_rolls_end}')