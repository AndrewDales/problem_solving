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
97,13,75,29,4"""

file_contents = test_data

file_orderings, file_sequences = test_data.split('\n\n')

def filter_ordering(sequence, ordering):
    """Remove any items in the ordering that are not in the sequence."""
    return [order for order in ordering if set(order) & set(sequence)]

data_ordering = tuple(tuple(int(i)for i in line.split("|")) for line in file_orderings.splitlines())
data_sequences = tuple(tuple(int(i)for i in line.split(",")) for line in file_sequences.splitlines())
