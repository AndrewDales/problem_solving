from math import sqrt
from textwrap import wrap
from typing import List

class BingoBoard:
    def __init__(self, board_list):
        self.board = board_list
        self.marked = [False] * len(board_list)
        self.size = int(sqrt(len(board_list)))
    
    def list_form(self, flat_list=None):
        if flat_list is None:
            flat_list = self.board
        return [flat_list[i:i+self.size] for i in range(0, len(flat_list), self.size)]
    
    def mark(self, num):
        try:
            idx = self.board.index(num)
            self.marked[idx] = True
        except ValueError:
            pass
    
    @property
    def unmarked_sum(self):
        return sum(el for el, mark_check in zip(self.board, self.marked)
                   if not mark_check) 
                
    @property
    def wins(self):
        # Check rows
        row_wins = [all(self.marked[i:i+self.size])
                    for i in range(0, len(self.marked), self.size)]
        col_wins = [all(self.marked[i::self.size])
                    for i in range(self.size)]
        return any(row_wins) or any(col_wins)
                    
    
    def __repr__(self):
        board_strings = ['\033[95m' + str(el) + '\033[0m' if bold else str(el)
                         for el, bold in zip(self.board, self.marked)]
        joined_strings = [" ".join(f'{el:>2}' for el in rs)
                          for rs in self.list_form(board_strings)]
        return "\n".join(joined_strings)


def find_winner(boards, calls):
    for call in calls:
        for board in boards:
            board.mark(call)
            if board.wins:
                return board, call

def find_loser(boards, calls):
    calls = iter(calls)
    unfinished_boards = boards.copy()
    while unfinished_boards:
        call = next(calls)
        for board in unfinished_boards:
            board.mark(call)
        unfinished_boards = [board for board in unfinished_boards if not board.wins]
    return board, call
    


with open("aoc_input_2021_4.txt", "r") as file:
    # Get the first line of bingo calls
    bingo_calls = file.readline().split(",")
    bingo_calls = [int(call) for call in bingo_calls]
    boards: List[List[int]] = []
    for line in file:
        # Start a new board each time there is an empty line
        if line == '\n':
            boards.append([])
        else:
            # Converts the line into a list of text width 3 (which each contain one number)
            line = wrap(line, 3)
            boards[-1] += [int(num) for num in line]
            
bingo_boards = [BingoBoard(board) for board in boards]
winning_board, final_call = find_winner(bingo_boards, bingo_calls)
losing_board, final_losing_call = find_loser(bingo_boards, bingo_calls)

print(f"Output Solution = {winning_board.unmarked_sum * final_call}")
print(f"Output Solution = {losing_board.unmarked_sum * final_losing_call}")
        