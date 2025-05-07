def l_system(level, sequence=None, rules=None):
    if sequence is None:
        sequence = 'F'
    if rules is None:
        rules = {'F': 'F+F-F+F'}

    if level == 0:
        return sequence

    else:
        new_sequence = ""
        for symbol in sequence:
            if symbol in rules:
                new_sequence += rules[symbol]
            else:
                new_sequence += symbol
        return l_system(level - 1, new_sequence, rules)


if __name__ == "__main__":
    koch_string = l_system(4)