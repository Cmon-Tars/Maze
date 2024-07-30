import unittest
from maze import Maze
from heap import MinHeap, Node

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
    
    def test_reset_visits(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(0,0,num_rows, num_cols, 10, 10)

    def test_heap(self):
        minheap = MinHeap()
        vals = [5,8,4,3,9,13,20]
        nodes = [Node(v) for v in vals]
        for n in nodes:
            minheap.addNode(n)
        for i, _ in enumerate(minheap.heap):
            if 2*i+1 < minheap.heapSize():
                if minheap.leftChild(i).val >= minheap.heap[i].val:
                    check_left = True
                else:
                    check_left = False
            if 2*i+2 < minheap.heapSize():
                if minheap.rightChild(i).val >= minheap.heap[i].val:
                    check_right = True
                else:
                    check_right = False

            self.assertEqual(check_left, True)
            self.assertEqual(check_right, True)

    def test_heap2(self):
            minheap = MinHeap()
            vals = [0,0,0]
            nodes = [Node(v) for v in vals]
            for n in nodes:
                minheap.addNode(n)
            for i, _ in enumerate(minheap.heap):
                if 2*i+1 < minheap.heapSize():
                    if minheap.leftChild(i).val >= minheap.heap[i].val:
                        check_left = True
                    else:
                        check_left = False
                if 2*i+2 < minheap.heapSize():
                    if minheap.rightChild(i).val >= minheap.heap[i].val:
                        check_right = True
                    else:
                        check_right = False

                self.assertEqual(check_left, True)
                self.assertEqual(check_right, True)
if __name__ == "__main__":
    unittest.main()
