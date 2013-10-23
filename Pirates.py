#!/usr/bin/env python3

import pygame
import pygame as pg

import grid
import ship

class PiratesGame:
    def __init__(self):
        self.cursor_x = 0
        self.cursor_y = 0
        def left(self):
            if self.cursor_x != 0:
                self.cursor_x -= 1
        def right(self):
            if self.cursor_x != 5:
                self.cursor_x += 1
        def down(self):
            if self.cursor_y != 5:
                self.cursor_y += 1
        def up(self):
            if self.cursor_y != 0:
                self.cursor_y -= 1
        self.key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up
        } # all commands
        self.grid = grid.Grid(6, 6)

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
            pygame.draw.rect(self.screen, (255, 0, 0), (self.grid.squares_to_pixels(self.cursor_x), self.grid.squares_to_pixels(self.cursor_y), 10, 10))
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
