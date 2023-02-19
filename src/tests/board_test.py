import os 
import sys
sys.path.append(os.path.abspath("."))

import unittest

from src.main.board import Board

class BoardTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        clues = {
            12:4,14:3,17:6,21:1,22:2,25:7,28:4,36:8,39:1,41:9,56:6,57:5,61:4,64:9,67:3,72:1,73:2,75:5,81:3,91:7,93:9,95:2,97:8,98:1
        }
        self.board = Board(clues)
        
    def test_next(self):
        curr = 10
        actual = self.board.next(10)
        print(f"Actual: {actual}")
        self.assertEqual(actual, 11)

  
if __name__ == '__main__':
    for p in sys.path:
        print("path --> "+ p)

    unittest.main()