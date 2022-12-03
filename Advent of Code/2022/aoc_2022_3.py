with open("aoc_2022_3.txt", "r") as file:
    contents = [line.strip() for line in file]


def find_repeat(content_code):
    n = len(content_code)
    return set(content_code[:n // 2]).intersection(set(content_code[n // 2:]))


def find_value(letter):
    offset = -ord('a') + 1 if letter.islower() else -ord('A') + 27
    return ord(letter) + offset


repeat_items = (find_repeat(code).pop() for code in contents)
print(f'Part 1 solution is {sum(find_value(let) for let in repeat_items)}')

elf_groups = ([set(contents[i]), set(contents[i + 1]), set(contents[i + 2])]
              for i in range(0, len(contents), 3))
badges = (elf[0].intersection(elf[1],elf[2]).pop()
          for elf in elf_groups)
print(f'Part 2 solution is {sum(find_value(badge) for badge in badges)}')
