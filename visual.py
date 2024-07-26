from tkinter import Canvas, Tk, BOTH

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = ""
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack()
        self.window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def drawLine(self, line, fill_color: str):
        self.window_running = True
        line.draw(canvas = self.canvas, fill_color=fill_color)

    def waitForClosed(self):
        self.window_running = True
        while self.window_running:
            self.redraw()

    def close(self):
        self.window_running = False
