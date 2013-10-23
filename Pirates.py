#!/usr/bin/env python3

import pygame
import pygame as pg

import grid
import ship

class PiratesGame:
    class State:
        def handle_key(self, game, key):
            if key in self.key_handlers:
                self.key_handlers[key](self, game)

    class SelectingSquareState (State):
        def __init__(self):
            self.cursor_x = 0
            self.cursor_y = 0
        def left(self, game):
            if self.cursor_x != 0:
                self.cursor_x -= 1

        def right(self, game):
            if self.cursor_x != game.grid.width - 1:
                self.cursor_x += 1

        def down(self, game):
            if self.cursor_y != game.grid.height - 1:
                self.cursor_y += 1

        def up(self, game):
            if self.cursor_y != 0:
                self.cursor_y -= 1

        key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up
        }
        
        def draw(self, game):
            pygame.draw.rect(game.screen, (255, 0, 0), (game.grid.squares_to_pixels(self.cursor_x), game.grid.squares_to_pixels(self.cursor_y), 10, 10))

    def __init__(self):
        self.state = self.SelectingSquareState()
        
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
                if event.type == pg.KEYDOWN:
                    self.state.handle_key(self, event.key)
                if event.type == pygame.QUIT:
                    self.running = False
            self.state.draw(self)
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
