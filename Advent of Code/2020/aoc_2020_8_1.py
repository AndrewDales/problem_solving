class Op:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
        self.executed = False
    
    def execute(self):
        self.executed = True
        line_delta = 1
        acc_delta = 0
        
        if self.operator == "jmp":
            line_delta = self.operand
        elif self.operator == "acc":
            acc_delta = self.operand
        
        return (line_delta, acc_delta)
    

program = {}
with open("aoc_2020_8.txt", "r") as file:
    for i, command_line in enumerate(file, 1):
        op, opr = command_line.split(" ")
        program[i] = Op(op, int(opr.strip()))

line = 1
acc = 0

current_command = program[1]

while not current_command.executed:
    ld, ac = current_command.execute()
    line += ld
    acc += ac
    current_command = program[line]
