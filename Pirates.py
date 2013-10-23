#!/usr/bin/env python3

import pygame
import pygame as pg

import grid
import ship

class PiratesGame:
    def __init__(self):
        self.grid = grid.Grid(6, 6)

        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor_pixelpos = [int(component) for component in self.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred=True)]

        def left(self):
            if self.cursor_x != 0:
                self.cursor_x -= 1
                self.cursor_pixelpos = [int(component) for component in self.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred=True)]
        def right(self):
            if self.cursor_x != self.grid.width - 1:
                self.cursor_x += 1
                self.cursor_pixelpos = [int(component) for component in self.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred=True)]
        def down(self):
            if self.cursor_y != self.grid.height - 1:
                self.cursor_y += 1
                self.cursor_pixelpos = [int(component) for component in self.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred=True)]
        def up(self):
            if self.cursor_y != 0:
                self.cursor_y -= 1
                self.cursor_pixelpos = [int(component) for component in self.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred=True)]
        self.key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up
        } # all commands

        self.running = False

    def run(self):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Yarrrr!!')

        while self.running:
            self.grid.draw(self.screen)
            for event in pygame.event.get():
                if event.type==pg.KEYDOWN and event.key in self.key_handlers:
                    self.key_handlers[event.key](self)
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.draw.circle(self.screen, (255, 0, 0), self.cursor_pixelpos, 10) # Draw cursor as a red circle
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
