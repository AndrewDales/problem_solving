num_spells = int(input())
spell_dict = {}
max_length = 0
max_length_count = 0


def cycle(n, p_spell_dict):
    current_page = n
    pages = set()
    while current_page not in pages:
        pages.add(current_page)
        current_page = p_spell_dict[current_page]
    complete_cycle = current_page == n
    return pages, complete_cycle


for i in range(num_spells):
    spell_dict[i + 1] = int(input())

starts = set(range(1, num_spells + 1))
while starts:
    page = starts.pop()
    current_cycle, complete = cycle(page, spell_dict)
    if len(current_cycle) > max_length:
        max_length = len(current_cycle)
        max_length_count = 0
    if len(current_cycle) == max_length:
        if complete:
            max_length_count += len(current_cycle)
        else:
            max_length_count += 1
    starts -= current_cycle

print(max_length)
print(max_length_count)

