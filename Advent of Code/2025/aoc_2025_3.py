with open('data/aoc_input_2025_3.txt', 'r') as file:
    data = [[int(d) for d in list(line.strip())] for line in file]

def max_digit(num_list: list[int]) -> tuple[int, int]:
    m = max(num_list)
    return m, num_list.index(m)

def max_value(num_list: list[int], digits) -> int:
    if digits == 1:
        return max(num_list)
    d, i = max_digit(num_list[:-(digits - 1)])
    return d * 10 ** (digits - 1) + max_value(num_list[i+1:], digits-1)

sum_jolts = sum(max_value(nums, 2) for nums in data)
sum_jolts_2 = sum(max_value(nums, 12) for nums in data)

print(f'Solution for part 1: {sum_jolts}')
print(f'Solution for part 2: {sum_jolts_2}')