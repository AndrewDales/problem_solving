num_spells = int(input())
spell_dict = {}


def cycle_length(n, p_spell_dict):
    current_page = n
    pages = set()
    while current_page not in pages:
        pages.add(current_page)
        current_page = p_spell_dict[current_page]
    return len(pages)


for i in range(num_spells):
    spell_dict[i + 1] = int(input())

cycle_lengths = [cycle_length(i, spell_dict) for i in range(1, num_spells + 1)]
max_length = max(cycle_lengths)
max_length_count = cycle_lengths.count(max_length)

print(max_length)
print(max_length_count)
