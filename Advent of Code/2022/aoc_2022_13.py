with open("aoc_2022_13.txt") as file:
    file_contents = [line.strip() for line in file]

packets = tuple((eval(file_contents[i]), eval(file_contents[i + 1])) for i in range(0, len(file_contents), 3))


def check_pair(lol_1, lol_2):

    # if all(isinstance(el, int) for el in lol_1 + lol_2):
    #     return lol_1 <= lol_2

    # Ran out of items on left
    if not lol_1:
        return True
    # Ran out of items on right
    elif not lol_2:
        return False

    left, right = lol_1[0], lol_2[0]

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if left > right:
            return False

    if isinstance(left, list) and isinstance(right, list):
        if left != right:
            return check_pair(left, right)

    else:
        if isinstance(left, int):
            left = [left]

        if isinstance(right, int):
            right = [right]

        # check_pair(left + lol_1[1:], right + lol_2[1:])
        if left != right:
            return check_pair(left, right)

    return check_pair(lol_1[1:], lol_2[1:])


correct_orders = [(i, check_pair(*packet)) for i, packet in enumerate(packets, 1)]
for i, packet in enumerate(packets, 1):
    print(i, check_pair(*packet))

print(sum(i for i, j in correct_orders if j))