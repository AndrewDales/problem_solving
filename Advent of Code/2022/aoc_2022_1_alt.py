data_sums = []

with open("aoc_2022_1.txt", "r") as file:
    total = 0
    for line in file:
        if line == '\n':
            data_sums.append(total)
            total = 0
        else:
            total += int(line)

print(max(data_sums))

data_sums.sort(reverse=True)

print(sum(data_sums[:3]))