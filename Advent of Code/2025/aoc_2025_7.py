import numpy as np

with open("data/aoc_input_2025_7.txt", 'r') as file:
    data = [list(line.strip()) for line in file]
    start_loc = data[0].index('S')
    data[0][start_loc] = "|"

data_np = np.array(data, dtype=str)
num_splits = 0

# Only need to consider every second row of the input data as odd rows are just all '.'
for i in range(2, len(data), 2):
    splitter_loc = data_np[i,:] == '^'
    beam_loc = data_np[i-2,:] == '|'

    # Where there are no splitters beams carry on as before
    data_np[i, beam_loc & ~splitter_loc] = '|'

    # Where splitters exist a new beam is created to either side of the old beam
    split_beams = splitter_loc & beam_loc
    num_splits += sum(split_beams)
    for j in np.argwhere(split_beams):
        data_np[i, [j-1, j+1]] = '|'

print(f'Solution to Day 7, part 1 is {num_splits}')

n, m = np.shape(data_np)
beams = np.zeros((n//2, m), dtype=int)
beams[0, start_loc] = 1

for i in range(2, len(data), 2):
    # Only calculate beams on odd rows
    j = i // 2
    splitter_loc = data_np[i,:] == '^'
    beam_loc = beams[j-1,:] > 0

    # Where there are no splitters the same number of beams carry on as in the previous row
    beams[j, beam_loc & ~splitter_loc] += beams[j-1, beam_loc & ~splitter_loc]

    # Where splitters exist the number of paths in the previous row is added to the paths before and after the splitter
    split_beams = splitter_loc & beam_loc
    for k in np.argwhere(split_beams):
        beams[j, [k-1, k+1]] += beams[j-1, k]

print(f'Solution to Day 7, part 2 is {sum(beams[-1,:])}')