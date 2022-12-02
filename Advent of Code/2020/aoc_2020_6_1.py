with open("aoc_2020_6.txt", "r") as file:
    raw_data = [line.strip() if len(line)> 1 else "!" for line in file]
    
data = "".join(raw_data).split("!")

number_of_codes = [len(set(code)) for code in data]

print(sum(number_of_codes))