from board import Board
from typing import Dict, Tuple

class SudokuResolver():

    def __init__(self, board: Board):
        self.b = board

    def print_board(self):
        """
        Prints the board with clues. The solution will be printed
        if the Sudoku is also resolved.
        """
        Board.print_board(self.b.get_board())
    
    def get_board(self) -> Dict[int, int]:
        return self.b.get_board()

    def resolve(self) -> Dict[int, int]:
        print("\n\nStarting execution...\n")
        return self.b.run()
    
    def run(self, callback) -> Tuple[int]:
        self.b.run(callback)

    def stop(self) -> None:
        self.b.stop()
