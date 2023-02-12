
import sys
from board import Board


class SudokuResolver():

    def __init__(self, board):
        self.b = board

    def resolve(self):
        Board.print_board(self.b.BOARD)
        print("\n\nStarting execution...\n")
        self.b.run()

def main():
    """
    create a Board
    add clues to the Board
    resolve
    """
    b = Board()
    resolver = SudokuResolver(b)
    resolver.resolve()

if __name__ == "__main__":
    main()
