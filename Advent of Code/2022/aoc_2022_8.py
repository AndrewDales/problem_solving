from _collections_abc import Iterable

with open("aoc_2022_8.txt") as file:
    trees = [[int(tree) for tree in list(line.strip())] for line in file]

n_rows = len(trees)
n_cols = len(trees[0])
count = 0


def number_before_blocked(tree_list: Iterable[int], p_current_tree: int) -> int:
    tree_count = 0
    # keep counting trees in the list
    for tree in tree_list:
        tree_count += 1
        # stop when you get to a tree at least as big as the current tree
        if tree >= p_current_tree:
            break
    return tree_count


max_tree_product = 0

for i in range(1,n_rows):
    for j in range(1,n_rows):
        left_trees = trees[i][:j]
        right_trees = trees[i][j + 1:]
        up_trees = [trees[k][j] for k in range(i)]
        down_trees = [trees[k][j] for k in range(i + 1, n_rows)]

        if left_trees:
            left_trees.reverse()
        if up_trees:
            up_trees.reverse()

        current_tree = trees[i][j]

        # Problem one
        if ((current_tree > max(left_trees, default=-1)) or
                (current_tree > max(right_trees, default=-1)) or
                (current_tree > max(up_trees, default=-1)) or
                (current_tree > max(down_trees, default=-1))):
            count += 1

        # Problem two
        tree_count_product = (number_before_blocked(left_trees, current_tree) *
                              number_before_blocked(right_trees, current_tree) *
                              number_before_blocked(up_trees, current_tree) *
                              number_before_blocked(down_trees, current_tree))

        if tree_count_product > max_tree_product:
            print(f'{i=},{j=},{current_tree=}{tree_count_product=}')
            max_tree_product = tree_count_product

print(f'Solution to Problem One is {count}')
print(f'Solution to Problem Two is {max_tree_product}')
