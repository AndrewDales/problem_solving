with open("aoc_2020_1.txt", "r") as file:
    numbers = [int(line.strip()) for line in file]
        
sum_2020_pairs = [(i,j, k) for i in numbers for j in numbers for k in numbers if i + j + k == 2020]

print(f"Solution is {sum_2020_pairs[0][0] * sum_2020_pairs[0][1] * sum_2020_pairs[0][2]}")