#!/usr/bin/env python3

import pygame
import pygame as pg

import grid
import ship

class PiratesGame:
    def __init__(self):
        self.x = 0
        self.y = 0
        def left(self):
            if self.x != 0:
                self.x -= 1
        def right(self):
            if self.x != 5:
                self.x += 1
        def down(self):
            if self.y != 5:
                self.y += 1
        def up(self):
            if self.y!=0:
                self.y -= 1
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
                    pygame.draw.rect((255, 0, 0), (10, 10, self.grid.squares_to_pixels(self.x), self.grid.squares_to_pixels(self.y)))
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
