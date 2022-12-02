from collections import defaultdict
from math import prod

with open("aoc_2020_3.txt", "r") as file:
    input_data = [line.strip()for line in file]

n_rows = len(input_data)
n_cols = len(input_data[0])
shifts = [(1, 1), (1, 3), (1,5), (1,7), (2,1)]

tree_dict = defaultdict(int)

for shift in shifts:
    i = 0
    j = 0
    while i < n_rows:
        if input_data[i][j] == "#":
            tree_dict[shift] += 1
        i += shift[0]
        j = (j + shift[1]) % n_cols

print(prod(tree_dict.values()))        
    
                  
    
    