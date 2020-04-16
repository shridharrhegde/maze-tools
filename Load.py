import core.maze as maz
import core.window as win

# params
maze_width = 16
cell_size = 20
wall_t = 1

# window size
win_size = (cell_size * maze_width, cell_size * maze_width)

# init window and maze
window = win.Window(win_size)
puzzle = maz.Maze(maze_width, cell_size, wall_t)

# load from file
puzzle.load("classic/apec_2010")

# draw on window
window.clear()
puzzle.draw(window.screen)

# handle basic events
while not window.closed:
    window.update()