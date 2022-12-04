with open("aoc_2020_2.txt", "r") as file:
    input_lines = [line.strip().split() for line in file]
        
parsed_lines = []
for line in input_lines:
    parsed_dict = dict()
    letter_range = line[0].split('-')
    parsed_dict["min"] = int(letter_range[0])
    parsed_dict["max"] = int(letter_range[1])
    parsed_dict["letter"] = line[1][0]
    parsed_dict["password"] = line[2]
    parsed_lines.append(parsed_dict)

num_correct = 0

for parsed_dict in parsed_lines:
    if parsed_dict["min"] <= parsed_dict["password"].count(parsed_dict["letter"]) <= parsed_dict["max"]:
        num_correct += 1
    
print(num_correct)
                  
    
    