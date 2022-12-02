with open("aoc_input_2021_3.txt", "r") as file:
    bin_input = [line.strip() for line in file]
        
column_sums = [sum(int(bin_input[i][j]) for i in range(len(bin_input)))
                                   for j in range(len(bin_input[0]))]

bin_digits = ["1" if cs > len(bin_input)//2 else "0" for cs in column_sums]
gamma = int("".join(bin_digits), 2)
mask = 2**len(bin_digits) - 1
epsilon = gamma ^ mask

print(f"Puzzle output: {epsilon*gamma}")
