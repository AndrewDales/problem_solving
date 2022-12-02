with open("aoc_input_2021_2.txt", "r") as file:
    directions = []
    for line in file:
        line = line.strip().split(" ")
        line[1] = int(line[1])
        directions.append(line)
        
# move_dir = {"forward": (1,0), "back": (0,1), "down": (0, 1), "up": (0, -1)}
position = {"depth": 0, "horizontal": 0, "aim": 0}

for command, distance  in directions:
    if command == "up":
        position["aim"] -= distance
    if command == "down":
        position["aim"] += distance
    if command == "forward":
        position["horizontal"] += distance
        position["depth"] += distance * position["aim"]
    
    
print(f'Puzzle output: {position["depth"] * position["horizontal"]}')