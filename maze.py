from shapes import Cell
import time
import random
import numpy as np

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

    def solve(self, i=0, j=0):
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
                solved = self.solve(n_idx[0], n_idx[1])
                if solved == True:
                    return True
                current.drawMove(to_cell, undo=True)
            elif direction == "down" and to_cell.has_top_wall == False and to_cell.visited == False:
                current.drawMove(to_cell)
                solved = self.solve(n_idx[0], n_idx[1])
                if solved == True:
                    return True
                current.drawMove(to_cell, undo=True)
            elif direction == "right" and to_cell.has_left_wall == False and to_cell.visited == False:
                current.drawMove(to_cell)
                solved = self.solve(n_idx[0], n_idx[1])
                if solved == True:
                    return True
                current.drawMove(to_cell, undo=True)
            else:
                if direction == "left" and to_cell.has_right_wall == False and to_cell.visited == False:
                    current.drawMove(to_cell)
                    solved = self.solve(n_idx[0], n_idx[1])
                    if solved == True:
                        return True
                    current.drawMove(to_cell, undo=True)
        return False


    
    # def solve(self, i=0,j=0, prev_cell=None, anim_speed=0.2):
    #     current = self.cells[i][j]
    #     current.visited = True
    #     neighbors = self.maze_graph[(i,j)]
    #     valid_moves = []
    #     for n in neighbors:
    #         direction = n[0]
    #         chosen_neighbor = n[1]
    #         to_cell = self.cells[chosen_neighbor[0]][chosen_neighbor[1]]
    #         if direction == "up":
    #             if to_cell.has_bottom_wall == False and to_cell.visited == False:
    #                 current.drawMove(to_cell)
    #                 self.animate(anim_speed)
    #                 self.solve(chosen_neighbor[0], chosen_neighbor[1], current)
    #         elif direction == "down":
    #             if to_cell.has_top_wall == False and to_cell.visited == False:
    #                 if to_cell == self.cells[-1][-1]:
    #                     current.drawMove(to_cell)
    #                     self.animate(anim_speed)
    #                     solved = True
    #                     print("top finish")
    #                 else:
    #                     current.drawMove(to_cell)
    #                     self.animate(anim_speed)
    #                     self.solve(chosen_neighbor[0], chosen_neighbor[1], current)
    #         elif direction == "right":
    #             if to_cell.has_left_wall == False and to_cell.visited == False:
    #                 if to_cell == self.cells[-1][-1]:
    #                     current.drawMove(to_cell)
    #                     self.animate(anim_speed)
    #                     print("right finish")
    #                     solved = True
    #                 else:
    #                     current.drawMove(to_cell)
    #                     self.animate(anim_speed)
    #                     self.solve(chosen_neighbor[0], chosen_neighbor[1], current)
    #         else:
    #             if to_cell.has_right_wall == False and to_cell.visited == False:
    #                 current.drawMove(to_cell)
    #                 self.animate(anim_speed)
    #                 self.solve(chosen_neighbor[0], chosen_neighbor[1], current)
    #         if to_cell == self.cells[-1][-1]:
    #             solved = True
    #             return 
    #     if prev_cell and solved == False:
    #         print("overwriting")
    #         current.drawMove(prev_cell, undo=True)
    #         self.animate(anim_speed)





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
                self.solve()
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
