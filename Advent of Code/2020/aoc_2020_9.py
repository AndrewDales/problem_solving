from collections import deque

with open("aoc_2020_9.txt", "r") as file:
    code_numbers = [int(line.strip()) for line in file]

n = 25
valid = True
previous_nums = deque(code_numbers[:n])
code_iter = iter(code_numbers[25:])
new_num: int = 0
invalid_pos: int = 0

# Part 1
while valid:
    valid_sums = [previous_nums[i] + previous_nums[j] for i in range(n) for j in range(i + 1, n)]
    new_num = next(code_iter)
    if new_num not in valid_sums:
        print(f"First invalid number is {new_num}")
        invalid_pos = code_numbers.index(new_num)
        valid = False
    else:
        previous_nums.popleft()
        previous_nums.append(new_num)

# Part 2
for i in range(invalid_pos):
    for j in range(i + 1, invalid_pos):
        if sum(code_numbers[i:j]) == new_num:
            max_val = max(code_numbers[i:j])
            min_val = min(code_numbers[i:j])
            print(f"Solution part 2 is {max_val + min_val}")
            break


