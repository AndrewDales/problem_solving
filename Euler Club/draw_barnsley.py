import turtle
import turtleBeads
from random import randint
from l_system import l_system

DEPTH = 7
side_length = 2


t_commands = {'F': lambda : turtle.forward(side_length),
            '+': lambda : turtle.left(randint(12,  28)),
            '-': lambda : turtle.right(randint(12, 28)),
            }

rules = {'F': 'FF',
         'X': 'F+[[X]-X]-F[-FX]+X',
        }

seed = '-X'

def draw_sequence(command_sequence, position=(-300, -300), bearing=90):
    def go_to_location(l_position, l_bearing):
        turtle.penup()
        turtle.setpos(l_position)
        turtle.setheading(l_bearing)
        turtle.pendown()

    go_to_location(position, bearing)
    position_stack = []

    for i, command in enumerate(command_sequence):
        if command in t_commands:
            t_commands[command]()
        if command == "[":
            position_stack.append((turtle.pos(), turtle.heading()))
        if command == "]":
            position, bearing = position_stack.pop()
            go_to_location(position, bearing)
    return

sequence = l_system(DEPTH, seed, rules)
print(sequence)

screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.bgcolor('#FAF8C8')
turtle.pencolor('green')
turtleBeads.noTrace()
draw_sequence(sequence)
turtle.hideturtle()
turtleBeads.showPicture()
turtle.done()