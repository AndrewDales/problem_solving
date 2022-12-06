with open("aoc_2022_6.txt") as file:
    code = file.readline().strip()

# 4 distinct characters for part 1, 14 for part 2
distinct_characters = 14

for i in range(distinct_characters, len(code)):
    if len(set(code[i-distinct_characters:i])) == distinct_characters:
        marker = i
        break
else:
    print('sequence of 4 different letters not found')
    marker = 0

print(marker)