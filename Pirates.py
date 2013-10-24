#!/usr/bin/env python3

import pygame
import pygame as pg

import grid
import ship

class PiratesGame:
    class State:
        def __init__(self, game):
            self.game = game

        def handle_key(self, key):
            if key in self.key_handlers:
                self.key_handlers[key](self)

        def update(self):
            pass

        def draw(self):
            pass

    class SelectingSquareState (State):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cursor_x = 0
            self.cursor_y = 0
            self.update_cursor()

        def update_cursor(self): # Updates the coordinates of the cursor
            self.cursor_pixelpos = self.game.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred = True, round = True)

        def left(self):
            if self.cursor_x != 0:
                self.cursor_x -= 1
                self.update_cursor()

        def right(self):
            if self.cursor_x != self.game.grid.width - 1:
                self.cursor_x += 1
                self.update_cursor()

        def down(self):
            if self.cursor_y != self.game.grid.height - 1:
                self.cursor_y += 1
                self.update_cursor()

        def up(self):
            if self.cursor_y != 0:
                self.cursor_y -= 1
                self.update_cursor()

        def enter(self):
            self.parent.child_return((self.cursor_x, self.cursor_y))

        key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up
        }

        def draw(self):
            self.parent.draw()
            pygame.draw.circle(self.game.screen, (255, 0, 0), self.cursor_pixelpos, 10) # Draw cursor as a red circle

    def __init__(self):
        self.grid = grid.Grid(6, 6)
        self.state = self.SelectingSquareState(self)
        self.running = False

    def run(self):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Yarrrr!!')

        while self.running:
            self.state.update()
            self.grid.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pg.KEYDOWN:
                    self.state.handle_key(event.key)
                if event.type == pygame.QUIT:
                    self.running = False
            self.state.draw()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
