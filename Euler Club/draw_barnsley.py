import turtle
import turtleBeads
from random import randint
from l_system import l_system, draw_sequence

DEPTH = 5
side_length = 2


t_commands = {'F': lambda : turtle.forward(side_length),
            '+': lambda : turtle.left(randint(12,  28)),
            '-': lambda : turtle.right(randint(12, 28)),
            }

rules = {'F': 'FF',
         'X': 'F+[[X]-X]-F[-FX]+X',
        }

seed = '-X'

sequence = l_system(DEPTH, seed, rules)
print(sequence)

screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.bgcolor('#FAF8C8')
turtle.pencolor('green')
turtleBeads.noTrace()
draw_sequence(sequence, t_commands)
turtle.hideturtle()
turtleBeads.showPicture()
turtle.done()