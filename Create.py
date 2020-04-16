"""
GUI for creating custom mazes
"""

import core.maze as maz
import core.window as win
import pygame

# params
maze_width = 16
cell_size = 20
wall_t = 1

# colors
prev_rect_color = (100, 200, 0)
next_rect_color = (0, 130, 220)


def main():
    # calculate window size
    win_size = (cell_size * maze_width, cell_size * maze_width)

    # initialize stuff
    window = win.Window(win_size)
    puzzle = maz.Maze(maze_width, cell_size, wall_t)
    clock = pygame.time.Clock()

    # flags and vars
    mouse_click = False
    mouse_prev = False
    idx, idy = (0, 0)
    mouse_rect = ()

    prev_idx, prev_idy = (0, 0)
    prev_rect = ()

    # previous actions
    actions = []

    while not window.closed:
        # event handling
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                puzzle.closed = True
                pygame.quit()
                return
            # keypress
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    # undo function
                    if not actions:
                        print("No more undos left")
                        continue
                    # get states
                    cell_1, vis_1 = actions.pop()
                    cell_2, vis_2 = actions.pop()
                    # reset visited states
                    cell_1.visited = vis_1
                    cell_2.visited = vis_2
                    # create wall
                    puzzle.create_wall(cell_1, cell_2)
                if event.key == pygame.K_s:
                    # save function
                    print("saving as maze.custom")
                    puzzle.save()
            # mouse left click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()[0]
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_click = False

        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        cels = puzzle.cell_size
        walt = puzzle.wall_t

        # divide screen to grid
        idx = int(mouse_pos[0] / cels)
        idy = int(mouse_pos[1] / cels)
        rect_mouse = (idx * cels, idy * cels, cels, cels)

        # mouse_click derivatives
        if mouse_click and not mouse_prev:
            # latch previous cell
            prev_idx, prev_idy = (idx, idy)
            prev_rect = rect_mouse
        if mouse_prev and not mouse_click:
            # get current states
            cell_1 = puzzle.get_cell(idx, idy)
            cell_2 = puzzle.get_cell(prev_idx, prev_idy)
            # save previous visited
            vis_1 = cell_1.visited
            vis_2 = cell_2.visited
            # set both cells as visited
            cell_1.visited = True
            cell_2.visited = True
            # remove walls
            puzzle.remove_wall(cell_1, cell_2)
            # push the previous states to actions
            actions.append((cell_1, vis_1))
            actions.append((cell_2, vis_2))
            # trim actions
            del actions[0:-10]

        # drawing on screen
        window.clear()
        puzzle.draw(window.screen)
        pygame.draw.rect(window.screen, next_rect_color, rect_mouse)
        pygame.draw.rect(window.screen, prev_rect_color, prev_rect) if mouse_click else None

        # update
        mouse_prev = mouse_click
        pygame.display.update()
        clock.tick(40)


if __name__ == "__main__":
    main()

