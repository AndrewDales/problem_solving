from collections import defaultdict

with open("aoc_2020_10.txt", "r") as file:
    jolt_numbers = [int(line.strip()) for line in file]

jolt_numbers.sort()
max_jolt = jolt_numbers[-1] + 3
jolt_numbers.append(max_jolt)

num_ways = defaultdict(int)
num_ways[0] = 1

for i in jolt_numbers:
    num_ways[i] = num_ways[i-1] + num_ways[i-2] + num_ways[i-3]

print(f'Solution is {num_ways[max_jolt]}')

