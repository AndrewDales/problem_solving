import re

with open('data/aoc_input_2024_3.txt') as file:
    file_contents = file.read()

# Problem 1
mul_statements = re.findall(r'mul\(\d+,\d+\)', file_contents)
mul_operands = [re.findall(r'\d+', statement) for statement in mul_statements]
sum_prod = sum(int(i) * int(j) for i, j in mul_operands)

# Problem 2
all_statements = re.findall(r"do\(\)|don't\(\)|mul\(\d+,\d+\)", file_contents)
total_prob_2 = 0
doing = True
for statement in all_statements:
    if statement == 'do()':
        doing = True
    elif statement == "don't()":
        doing = False
    elif doing:
        i, j = re.findall(r'\d+', statement)
        total_prob_2 += int(i) * int(j)



print(f'Solution to Advent of Code 2024, problem 3a is {sum_prod}')
print(f'Solution to Advent of Code 2024, problem 3b is {total_prob_2}')