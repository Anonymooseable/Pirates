import circuits
import grid
from state import State
import pygame
import pygame as pg

class SelectionConfirmed (circuits.Event):
    """Fired when the selection of a square is confirmed by the user"""
    def __init__(self, selection):
        super().__init__()
        self.selection = selection

class SelectingSquareState (State):
    def __init__(self):
        super().__init__()
        self.cursor_x = 0
        self.cursor_y = 0

    def update_cursor(self): # Updates the coordinates of the cursor
        self.cursor_pixelpos = self.root.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred = True, round = True)

    def registered(self, *args):
        self.update_cursor()

    def left(self):
        if self.cursor_x != 0:
            self.cursor_x -= 1
            self.update_cursor()

    def right(self):
        if self.cursor_x != self.parent.grid.width - 1:
            self.cursor_x += 1
            self.update_cursor()

    def down(self):
        if self.cursor_y != self.parent.grid.height - 1:
            self.cursor_y += 1
            self.update_cursor()

    def up(self):
        if self.cursor_y != 0:
            self.cursor_y -= 1
            self.update_cursor()

    def enter(self):
        self.fire(SelectionConfirmed((self.cursor_x, self.cursor_y)))
        self.unregister()

    keydown_handlers = {
        pg.K_LEFT: left,
        pg.K_RIGHT: right,
        pg.K_DOWN: down,
        pg.K_UP: up,
        pg.K_RETURN: enter
    }

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.circle(surface, (255, 0, 0), self.cursor_pixelpos, 10) # Draw cursor as a red circle
