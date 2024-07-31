from shapes import Cell
import time
import random
import numpy as np
from heap import MinHeap, Node

class Maze:
    def __init__(self, x1, y1, num_cols, num_rows, cell_size_x, cell_size_y, win=None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cells = None
        self.win = win
        self.maze_creation_error = None
        self.maze_graph = {}
        if seed:
            random.seed(seed)
        self.createCells()

    def solve(self, algo="dfs"):
        if algo == "dfs":
            self.dfs()
        if algo == "A*":
            self.aStar()

    def showPath(self, came_from, current):
        path = [current]
        while current in came_from.keys():
            current = came_from[current]
            path.insert(0,current)
        for i, s in enumerate(path):
            if i+1 < len(path):
                current = self.cells[s[0]][s[1]]
                tc_idx = path[i+1]
                to_cell = self.cells[tc_idx[0]][tc_idx[1]]
            current.drawMove(to_cell)

    def taxicabDist(self,i,j):
        return (self.num_cols-i) + (self.num_rows-j) - 2

    def aStar(self, ):
        heap = MinHeap()
        came_from = {}
        gscore = {}
        fscore = {}
        d = 1
        for k in self.maze_graph:
            gscore[k] = float("inf")
            fscore[k] = float("inf")
        gscore[(0,0)] = 0
        fscore[(0,0)] = gscore[(0,0)] + self.taxicabDist(0,0)
        heap.addNode(Node(fscore[(0,0)],(0,0)))
        while heap.heapSize() > 0:
            current = heap.getMin()
            if current.data == (self.num_cols-1, self.num_rows-1):
                self.showPath(came_from, current.data)
            heap.removeMin()
            neighbors = self.maze_graph[current.data]
            for n in neighbors:
                valid = False
                direction, n_idx = n[0], n[1]
                if direction == "up" and self.cells[n_idx[0]][n_idx[1]].has_bottom_wall == False:
                    valid = True
                elif direction == "down" and self.cells[n_idx[0]][n_idx[1]].has_top_wall == False:
                    valid = True  
                elif direction == "right" and self.cells[n_idx[0]][n_idx[1]].has_left_wall == False:
                    valid = True
                else:
                    if direction == "left" and self.cells[n_idx[0]][n_idx[1]].has_right_wall == False:
                        valid = True
                if valid:
                    tentative_gscore = gscore[current.data] + d
                    if tentative_gscore < gscore[n_idx]:
                        came_from[n_idx] = current.data
                        gscore[n_idx] = tentative_gscore
                        fscore[n_idx] = gscore[n_idx] + self.taxicabDist(*n_idx)
                        if Node(fscore[n_idx], n_idx) not in heap.heap:
                            heap.addNode(Node(fscore[n_idx], n_idx))
                else:
                    valid = False
        return

    def dfs(self, i=0, j=0):
        self.animate(0.002)
        current = self.cells[i][j]
        if current == self.cells[-1][-1]:
            return True
        current.visited = True
        neighbors = self.maze_graph[(i,j)]
        for n in neighbors:
            direction = n[0]
            n_idx=n[1]
            to_cell = self.cells[n_idx[0]][n_idx[1]]
            if direction == "up" and to_cell.has_bottom_wall == False and to_cell.visited == False:
                current.drawMove(to_cell)
                solved = self.dfs(n_idx[0], n_idx[1])
                if solved == True:
                    return True
                current.drawMove(to_cell, undo=True)
            elif direction == "down" and to_cell.has_top_wall == False and to_cell.visited == False:
                current.drawMove(to_cell)
                solved = self.dfs(n_idx[0], n_idx[1])
                if solved == True:
                    return True
                current.drawMove(to_cell, undo=True)
            elif direction == "right" and to_cell.has_left_wall == False and to_cell.visited == False:
                current.drawMove(to_cell)
                solved = self.dfs(n_idx[0], n_idx[1])
                if solved == True:
                    return True
                current.drawMove(to_cell, undo=True)
            else:
                if direction == "left" and to_cell.has_right_wall == False and to_cell.visited == False:
                    current.drawMove(to_cell)
                    solved = self.dfs(n_idx[0], n_idx[1])
                    if solved == True:
                        return True
                    current.drawMove(to_cell, undo=True)
        return False

    def createCells(self):
        # i is number of columns (x-direction)
        # j is number of rows (y-direction)
        self.cells = []
        if self.num_rows > 0 and self.num_cols > 0:
            for i in range(0, self.num_cols):
                column = []
                for j in range(0, self.num_rows):
                    self.maze_graph[(i,j)] = None
                    column.append(Cell(self.win))
                self.cells.append(column)
            if self.win:
                for i, cols in enumerate(self.cells):
                    for j, _ in enumerate(cols):
                        self.drawCell(i, j)
                self.breakEntranceAndExit()
                self.buildGraph()
                self.breakWalls()
                self.resetVisited()
                self.solve(algo="A*")
                #self.showGraph()
            else: #For testing purposes
                for i, cols in enumerate(self.cells):
                    for j, _ in enumerate(cols):
                        self.updateCell(i, j)
                self.updateEntranceAndExit()
        else:
            self.maze_creation_error = f"Cannot create maze matrix with {self.num_rows} rows and {self.num_cols} columns"
    
    def showGraph(self):
        for k,v in self.maze_graph.items():
            print(f"node: {k} | values: {v}")
        
    def breakEntranceAndExit(self):
        entrance_cell, exit_cell = self.updateEntranceAndExit()
        entrance_cell.draw()
        exit_cell.draw()
        self.animate()
    
    def resetVisited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def updateEntranceAndExit(self):
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]
        entrance_cell.has_left_wall = False
        exit_cell.has_right_wall = False
        return entrance_cell, exit_cell

    def updateCell(self, i, j):
        cell = self.cells[i][j]
        x_pos = self.x1 + i*self.cell_size_x
        y_pos = self.y1 + j*self.cell_size_y
        cell.has_left_wall, cell.has_right_wall, cell.has_top_wall, cell.has_bottom_wall = [True, True, True, True]
        cell.x1 = x_pos 
        cell.y1 = y_pos
        cell.x2 = x_pos + self.cell_size_x
        cell.y2 = y_pos + self.cell_size_y
        return cell
    
    def buildGraph(self):
        for k in self.maze_graph:
            neighbors = []
            i = k[0]
            j = k[1]
            if  i-1 >= 0:
                neighbors.append(["left", (i-1, j)])
            if i+1 <= len(self.cells)-1:
                neighbors.append(["right",(i+1, j)])
            if j-1 >= 0:
                neighbors.append(["up", (i, j-1)])
            if j+1 <= len(self.cells[i])-1:
                neighbors.append(["down", (i, j+1)])
            self.maze_graph[k] = neighbors
    
    def breakWalls(self, i=0, j=0):
        current_cell = self.cells[i][j]
        current_cell.visited = True
        while True:
            possible_directions = [x[1] for x in self.maze_graph[(i,j)]]
            valid_directions = [pd for pd in possible_directions if self.cells[pd[0]][pd[1]].visited == False]
            if valid_directions:
                direction = valid_directions[random.randint(0, len(valid_directions)-1)]
                next_cell = self.cells[direction[0]][direction[1]]
                if direction[0] == i:
                    if j - direction[1] < 0:
                        current_cell.has_bottom_wall = False
                        next_cell.has_top_wall = False
                    else:
                        current_cell.has_top_wall = False
                        next_cell.has_bottom_wall = False
                else:
                    if i - direction[0] < 0:
                        current_cell.has_right_wall = False
                        next_cell.has_left_wall = False
                    else:
                        current_cell.has_left_wall = False
                        next_cell.has_right_wall = False
            else:
                return
            current_cell.draw()
            self.animate()
            self.breakWalls(i=direction[0], j=direction[1])

    def drawCell(self, i, j, fill_color = "black"):
        cell = self.updateCell(i,j)
        cell.draw(fill_color)
        self.animate(.0005)

    def animate(self, sleep_time=0.005):
        self.win.redraw()
        time.sleep(sleep_time)
