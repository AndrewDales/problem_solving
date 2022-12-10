with open("aoc_2022_8.txt") as file:
    trees = [[int(tree) for tree in list(line.strip())] for line in file]

n_rows = len(trees)
n_cols = len(trees[0])
count = 0

for i in range(n_rows):
    for j in range(n_rows):
        left_trees = trees[i][:j]
        right_trees = trees[i][j+1:]
        up_trees = [trees[k][j] for k in range(i)]
        down_trees = [trees[k][j] for k in range(i+1, n_rows)]

        current_tree = trees[i][j]

        if ((current_tree > max(left_trees,default=-1)) or
            (current_tree > max(right_trees, default=-1)) or
            (current_tree > max(up_trees, default=-1)) or
            (current_tree > max(down_trees, default=-1))
            ):
            count += 1

print(f'Solution to Problem One is {count}')
