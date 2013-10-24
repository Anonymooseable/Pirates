import circuits
import pygame
import pygame as pg

import grid
from .state import State

class CursorState (State):
    def __init__(self):
        super().__init__()
        self.cursor_x = 0
        self.cursor_y = 0

        def move_cursor_function(fun): # Decorator for functions that move the cursor
            def result(self):
                fun(self)
                self.update_cursor()
            return result

        @move_cursor_function
        def left(self):
            if self.cursor_x != 0:
                self.cursor_x -= 1

        @move_cursor_function
        def right(self):
            if self.cursor_x != self.parent.grid.width - 1:
                self.cursor_x += 1

        @move_cursor_function
        def down(self):
            if self.cursor_y != self.parent.grid.height - 1:
                self.cursor_y += 1

        @move_cursor_function
        def up(self):
            if self.cursor_y != 0:
                self.cursor_y -= 1

        self.keydown_handlers.update({
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up,
        })

    def update_cursor(self): # Updates the coordinates (in pixels) of the cursor
        self.cursor_pixelpos = self.root.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred = True, round = True)

    def registered(self, *args):
        self.update_cursor()

