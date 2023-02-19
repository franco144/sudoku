from board import Board

class SudokuResolver():

    def __init__(self, board):
        self.b = board

    def print(self):
        Board.print_board(self.b.BOARD)
        print("\n\nStarting execution...\n")
        
    def resolve(self):
        self.b.run()
