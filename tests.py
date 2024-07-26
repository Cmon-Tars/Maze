import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(0,0,num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1.cells[0]), num_cols)
        self.assertEqual(len(m1.cells), num_rows)

    def test_maze_create_cells2(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0,0,num_cols, num_rows, 10, 10)
        self.assertEqual(len(m1.cells[0]), num_cols)
        self.assertEqual(len(m1.cells), num_rows)
    
    def test_maze_create_cells3(self):
        num_cols = 0
        num_rows = 1
        m1 = Maze(0,0,num_cols, num_rows, 10, 10)
        self.assertEqual(f"Cannot create maze matrix with {num_rows} rows and {num_cols} columns", m1.maze_creation_error)
    
    def test_maze_create_cells4(self):
        num_cols = 1
        num_rows = 0
        m1 = Maze(0,0, num_cols, num_rows, 10, 10)
        self.assertEqual(f"Cannot create maze matrix with {num_rows} rows and {num_cols} columns", m1.maze_creation_error)

    def test_maze_entrance_and_exit(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(0,0, num_cols, num_rows, 10, 10)
        self.assertEqual(m1.cells[0][0].has_left_wall, False)
        self.assertEqual(m1.cells[-1][-1].has_right_wall, False)
    
    #def test_maze_entrance_and_exit(self):
     #   num_cols = 10
     #   num_rows = 12
      #  m1 = Maze(0,0,num_rows, num_cols, 10, 10)
if __name__ == "__main__":
    unittest.main()
