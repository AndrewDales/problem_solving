with open("aoc_input_2021_2.txt", "r") as file:
    directions = []
    for line in file:
        line = line.strip().split(" ")
        line[1] = int(line[1])
        directions.append(line)
        
move_dir = {"forward": (1,0), "back": (0,1), "down": (0, 1), "up": (0, -1)}
position = [0, 0]

for command in directions:
    move_vec = [x * command[1] for x in move_dir[command[0]]]
    position = [sum(p) for p in zip(position, move_vec)]
    
print(f'Puzzle output: {position[0] * position[1]}')