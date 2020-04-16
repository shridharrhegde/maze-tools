"""
WINDOW CLASS
"""

import pygame


class Window:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.closed = False

    def update(self):
        if self.closed:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.closed = True
                pygame.quit()
                return

        pygame.display.update()
        self.clock.tick(40)

    def fill(self, color):
        self.screen.fill(color)

    def clear(self):
        # fill screen with white
        self.screen.fill((255, 255, 255))

