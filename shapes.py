from tkinter import Canvas
from visual import Window

class Point:
    def __init__(self, x: int =0, y: int =0):
        # Defaulted to the top left
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2
    
    def __repr__(self) -> str:
        return f"Line from {self.point1} to {self.point2}"
    
    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill = fill_color, width=2)

class Cell:
    def __init__(self, win: Window = None):
        self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bottom_wall =  [None for _ in range(4)]
        self.x1 = None
        self.val = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.win = win
        self.visited = False
    
    def __repr__(self) -> str:
        return f"Cell Walls: {[self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bottom_wall]}"
    
    def draw(self, fill_color: str = "black"):
        if self.has_left_wall:
            line = Line(Point(self.x1, self.y1),  Point(self.x1, self.y2))
            self.win.drawLine(line, fill_color)
        else:
            line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self.win.drawLine(line, "#d9d9d9")
        if self.has_right_wall:
            line = Line(Point(self.x2, self.y2), Point(self.x2, self.y1))
            self.win.drawLine(line, fill_color)
        else:
            line = line = Line(Point(self.x2, self.y2), Point(self.x2, self.y1))
            self.win.drawLine(line, "#d9d9d9")
        if self.has_top_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.win.drawLine(line, fill_color)
        else:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.win.drawLine(line, "#d9d9d9")
        if self.has_bottom_wall:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.win.drawLine(line, fill_color)
        else:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.win.drawLine(line, "#d9d9d9")
            
    def drawMove(self, to_cell, undo=False):
        cell_size_x = self.x2-self.x1
        cell_size_y = self.y2-self.y1
        current_point = Point(self.x2-(cell_size_x)/2, self.y2-(cell_size_y/2))
        next_point = Point(to_cell.x2-(cell_size_x)/2, to_cell.y2-(cell_size_y/2))
        line = Line(current_point, next_point)
        if not undo:
            self.win.drawLine(line, "red")
        else:
            self.win.drawLine(line, "gray")
