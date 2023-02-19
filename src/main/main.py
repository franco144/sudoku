
import sys
from board import Board
from sudokuresolver import SudokuResolver

def run():
    """
    create a Board
    add clues to the Board
    resolve
    """
    clues = {
        12:4,14:3,17:6,21:1,22:2,25:7,28:4,36:8,39:1,41:9,56:6,57:5,61:4,64:9,67:3,72:1,73:2,75:5,81:3,91:7,93:9,95:2,97:8,98:1
    }
    b = Board(clues)
    
    resolver = SudokuResolver(b)
    resolver.print()
    # resolver.resolve()

# if __name__ == "__main__":
#     run()
