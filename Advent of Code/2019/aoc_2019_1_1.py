with open("data/aoc_input_2019_1.txt", "r") as file:
    numbers = [int(line.strip()) for line in file]


def total_fuel(fuel_n: int):
    fuel_step = fuel_n
    total = 0

    while (fuel_step := fuel_step // 3 - 2) > 0:
        total += fuel_step

    return total


# Part 1
print(f'Answer to part 1: {sum(i // 3 - 2 for i in numbers)}')

# Testing
assert total_fuel(14) == 2
assert total_fuel(1969) == 966
assert total_fuel(100756) == 50346

# Part 2
print(f'Answer to part 2: {sum(total_fuel(i) for i in numbers)}')
