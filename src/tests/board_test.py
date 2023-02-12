import os 
import sys
sys.path.append(os.path.abspath("."))

import unittest

from sudoku.src.main.board import Board

class BoardTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.board = Board()
        
    def test_next(self):
        curr = 10
        actual = self.board.next(10)
        print(f"Actual: {actual}")
        self.assertEqual(actual, 11)

  
if __name__ == '__main__':
    print(sys.path)
    unittest.main()