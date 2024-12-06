test_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

with open('data/aoc_input_2024_5.txt', 'r') as file:
    file_contents = file.read()

# file_contents = test_data

file_orderings, file_sequences = file_contents.split('\n\n')

def filter_ordering(sequence, ordering):
    """Remove any items in the ordering that are not in the sequence."""
    return [order for order in ordering if (order[0] in sequence and order[1] in sequence)]

def test_sequence(sequence, ordering):
    mis_ordering = False
    while sequence and not mis_ordering:
        filtered_ordering = filter_ordering(sequence, ordering)
        val, sequence = sequence[0], sequence[1:]
        if any(val == order[1] for order in filtered_ordering):
            mis_ordering = True
    return mis_ordering

def find_start(sequence, ordering):
    for s in sequence:
        if not any(s == order[1] for order in ordering):
            return s

def order_sequence(sequence, ordering):
    if len(sequence) == 1:
        ordered_sequence = sequence
    else:
        filtered_ordering = filter_ordering(sequence, ordering)
        s = find_start(sequence, filtered_ordering)
        sequence = tuple(val for val in sequence if val != s)
        ordered_sequence = (s,) + order_sequence(sequence, filtered_ordering)
    return ordered_sequence

middle_values = 0
middle_values_ordered = 0
data_ordering = tuple(tuple(int(i)for i  in line.split("|")) for line in file_orderings.splitlines())
data_sequences = tuple(tuple(int(i)for i in line.split(",")) for line in file_sequences.splitlines())

test_sequence(data_sequences[0], data_ordering)
for seq in data_sequences:
    if not test_sequence(seq, data_ordering):
        middle_values += seq[len(seq)//2]
    else:
        ordered_seq = order_sequence(seq, data_ordering)
        middle_values_ordered += ordered_seq[len(ordered_seq)//2]

print(f'Solution to Day 5a is {sum(middle_values)}')
print(f'Solution to Day 5b is {sum(middle_values_ordered)}')