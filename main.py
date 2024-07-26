from visual import Window
from maze import Maze

def main():
    window_width = 100
    window_height = 100
    win = Window(window_width, window_height)
    num_cols = 4
    num_rows = 4
    cell_size_x =  10
    cell_size_y =  10
    maze = Maze(x1 = round((window_width - num_cols*cell_size_x)/2), y1 = round((window_height - num_rows*cell_size_y)/2), num_cols = num_cols, num_rows = num_rows, cell_size_x =cell_size_x, cell_size_y =cell_size_y, win = win, seed=0)
    win.waitForClosed()

if __name__ == "__main__":
    main()