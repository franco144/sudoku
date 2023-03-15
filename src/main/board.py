import time
import sys
from typing import Dict

"""
-------------------------------
| 8  4  7 | 3  9  1 | 6  2  5 |
| 1  2  3 | 6  7  5 | 9  4  8 |
| 5  9  6 | 2  4  8 | 7  3  1 |
-------------------------------
| 9  7  8 | 5  3  4 | 1  6  2 |
| 2  3  1 | 7  8  6 | 5  9  4 |
| 4  6  5 | 9  1  2 | 3  8  7 |
-------------------------------
| 6  1  2 | 8  5  9 | 4  7  3 |
| 3  8  4 | 1  6  7 | 2  5  9 |
| 7  5  9 | 4  2  3 | 8  1  6 |
-------------------------------
"""

class Board():
    BOARD = {
        11:  0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0,
        21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0,
        31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0,
        41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0,
        51: 0, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0,
        61: 0, 62: 0, 63: 0, 64: 0, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0,
        71: 0, 72: 0, 73: 0, 74: 0, 75: 0, 76: 0, 77: 0, 78: 0, 79: 0,
        81: 0, 82: 0, 83: 0, 84: 0, 85: 0, 86: 0, 87: 0, 88: 0, 89: 0,
        91: 0, 92: 0, 93: 0, 94: 0, 95: 0, 96: 0, 97: 0, 98: 0, 99: 0
    }

    def __init__(
        self, 
        clues: Dict[int, int]
    ) -> None:
        self.loop = True
        self.start_time = None
        self.end_time = None
        self.curr = 10  # index of the 'zero cell'
        # self.clues = [12,14,17,21,22,25,28,36,39,41,56,57,61,64,67,72,73,75,81,91,93,95,97,98] 
        # self.clues_values = {
        #    12:4,14:3,17:6,21:1,22:2,25:7,28:4,36:8,39:1,41:9,56:6,57:5,61:4,64:9,67:3,72:1,73:2,75:5,81:3,91:7,93:9,95:2,97:8,98:1
        # }
        self.clue_cells = clues.keys() # indexes of clue cells
        self.cells = [] # LIFO with indexes of non clue cells
        
        for cell in self.BOARD.keys():
            if cell in self.clue_cells:
                self.BOARD[cell] = clues[cell]

        print(f"self.clues: {self.clue_cells}")
        print(f"cells to fill: {[i for i in Board.BOARD.keys() if i not in self.clue_cells]}")

    def get_board(self) -> Dict[int, int]:
        return self.BOARD

    def stop(self):
        self.loop = False

    def run(self, callback=None) -> Dict[int, int]:
        """
        get cell
        get value of cell
        while value < 9
            increase value of 1
            check value for violations
                if OK
                    store value in cells
                    break
        if value == 9 #backtrack
            set value to 0
            store value in cells
            get prev cell
        """
        self.callback = callback or fallback
        dir = 1
        Board.print_board(self.BOARD)
        self.start_time = time.time()
        while self.loop:
            # move cell
            if dir == 1:
                self.curr = self.next(self.curr)
            elif dir == -1:
                self.curr = self.prev(self.curr)
            else:
                Board.print_board(self.BOARD)
                raise Exception(f"Invalid value for dir {dir}")

            # read value in cell
            value = self.BOARD[self.curr]
            dir = 0
            while value < 9:
                value += 1
                # check that value do not violate any constraint
                if self.isValid(self.curr, value):
                    self.BOARD[self.curr] = value
                    self.callback(self.curr, value)
                    dir = 1
                    # check if last cell of the board is reached
                    if self.curr == 99:
                        self.end_time = time.time()
                        Board.print_board(self.BOARD)
                        print("Reached last cell successfully!")
                        self.callback(self.curr, None)
                        self.stop()
                    
                    break
            
            if value == 9 and dir == 0:
                #backtracking
                self.BOARD[self.curr] = 0
                self.callback(self.curr, value)
                dir = -1
                if self.curr == 11:
                    Board.print_board(self.BOARD)
                    raise Exception("Reached 9 on first cell and moving back") 
        
        print(f"Execution time in seconds {self.end_time-self.start_time}")


    def isValid(self, cell, num):
        row = str(cell)[:1]
        col = str(cell)[1:]
        # check if num is in col
        for r in range(1,10):
            if str(r) == row:
                continue
            if self.BOARD[int(str(r)+col)] == num:
                return False
        
        # check if num is in row
        for c in range(1,10):
            if str(c) == col:
                continue
            if self.BOARD[int(row+str(c))] == num:
                return False

        # check if num is in cell's box
        for i in [11,14,17,41,44,47,71,74,77]:
            if int(row) >= int(str(i)[:1]) and int(row) <= (int(str(i)[:1])+2):
                if int(col) >= int(str(i)[1:]) and int(col) <= (int(str(i)[1:])+2):
                    # i is the top left cell of the box where num is
                    for ir in range(int(str(i)[:1]), int(str(i)[:1])+3):
                        for ic in range(int(str(i)[1:]), int(str(i)[1:])+3):
                            if ir == int(row) and ic == int(col):
                                continue
                            if self.BOARD[int(str(ir)+str(ic))] == num:
                                return False
        return True                    

    def next(self, curr):
        if curr == 99:
            raise Exception("No next found. Current is last cell: 99")
        elif str(curr)[1:] == '9':
            res = curr + 2
        else:
            res = curr + 1
        # check if cell is one of the clues
        if res in self.clue_cells:
            return self.next(res)

        self.cells.append(res)
        print(f"(next) cells -> {self.cells}")
        return res

    def prev(self, curr):        
        self.cells.pop() # remove current

        print(f"(prev) cells -> {self.cells}")

        res = self.cells[-1]
        if res == 11:
            print("Reached first cell")
        return res

    @staticmethod
    def print_board(b1):
        print()
        for r in range(1,10):
            if r == 1 or r == 4 or r == 7:
                print("-------------------------------")
            for c in range(1,10):
                if c == 1 or c == 4 or c == 7:
                    print("|", end="")
                print(f" {str(b1[int(str(r)+str(c))])} ", end="")
                # if c % 3 == 0:
                #     print("|", end="")
                if c % 9 == 0:
                    print("|\n", end="")
        print("-------------------------------")
    

def fallback(curr_cell:int, value:int):
    pass
