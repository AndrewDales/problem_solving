import turtle

turtle.speed(0)

def l_system(level, sequence=None, rules=None):
    """ Creates a Lindenmayer sequence of level, level, given an initial sequence and a dictionary of rules."""
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

def draw_sequence(command_sequence, commands, position=(-300, -300), bearing=90):
    """ Draws a Lindenmayer sequence in Python turtle"""
    def go_to_location(l_position, l_bearing):
        turtle.penup()
        turtle.setpos(l_position)
        turtle.setheading(l_bearing)
        turtle.pendown()

    go_to_location(position, bearing)
    position_stack = []

    for i, command in enumerate(command_sequence):
        if command in commands:
            commands[command]()
        elif command == "[":
            position_stack.append((turtle.pos(), turtle.heading()))
        elif command == "]":
            position, bearing = position_stack.pop()
            go_to_location(position, bearing)
    return


if __name__ == "__main__":
    koch_string = l_system(4)