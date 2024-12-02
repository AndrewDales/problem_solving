
with open("data/aoc_input_2024_1.txt") as file:
    file_contents = file.readlines()

locations_1 = []
locations_2 = []

for line in file_contents:
    i, j = line.strip().split('   ')
    locations_1.append(int(i))
    locations_2.append(int(j))

locations_1.sort()
locations_2.sort()

sum_differences = sum(abs(i-j) for i, j in zip(locations_1, locations_2))
similarity_score = sum(locations_2.count(i) * i for i in locations_1)

print(f'Solution to Advent of Code 2024, problem 1a is {sum_differences}')
print(f'Solution to Advent of Code 2024, problem 1b is {similarity_score}')