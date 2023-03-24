
import sys
from board import Board
from sudokuresolver import SudokuResolver

def run(headless=False):
    """
    create a Board
    add clues to the Board
    resolve
    """
    # clues = {
    #     12:4,14:3,17:6,21:1,22:2,25:7,28:4,36:8,39:1,41:9,56:6,57:5,61:4,64:9,67:3,72:1,73:2,75:5,81:3,91:7,93:9,95:2,97:8,98:1
    # }
    clues = {
        15:3,23:8,24:7,31:3,38:7,39:2,
        41:8,42:4,45:1,46:9,49:3,52:6,62:9,64:2,
        71:7,76:5,78:6,79:9,83:4,87:3,91:1,94:4,99:8
    }
    b = Board(clues)
    
    resolver = SudokuResolver(b)
    resolver.print_board()

    # check if it's running without GUI
    if headless:
        resolver.resolve()

if __name__ == "__main__":
    run(True)
