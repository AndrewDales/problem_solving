with open("aoc_2020_6.txt", "r") as file:
    raw_data = [line.strip() if len(line)> 1 else "!" for line in file]
    
data = " ".join(raw_data).split("!")

data_lists = [line.strip().split(" ") for line in data]
data_sets = [[set(word) for word in line] for line in data_lists]

data_set_intersects = [data_set[0].intersection(*data_set[1:])
                       for data_set in data_sets]
    
print(sum(len(dsi) for dsi in data_set_intersects))