from visual import Window
from maze import Maze

def main():
    window_width = 900
    window_height = 900
    win = Window(window_width, window_height)
    num_cols = 40
    num_rows = 40
    cell_size_x =  20
    cell_size_y =  20
    maze = Maze(x1 = round((window_width - num_cols*cell_size_x)/2), y1 = round((window_height - num_rows*cell_size_y)/2), num_cols = num_cols, num_rows = num_rows, cell_size_x =cell_size_x, cell_size_y =cell_size_y, win = win, seed=0)
    win.waitForClosed()

if __name__ == "__main__":
    main()