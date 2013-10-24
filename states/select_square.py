import circuits
import pygame
import pygame as pg

import grid
from .cursor_state import CursorState

class SelectionConfirmed (circuits.Event):
    """Fired when the selection of a square is confirmed by the user"""
    def __init__(self, selection):
        super().__init__()
        self.selection = selection

class SelectingSquareState (CursorState):
    def __init__(self):
        super().__init__()
        def enter(self):
            self.fire(SelectionConfirmed((self.cursor_x, self.cursor_y)))
            self.unregister()
        self.keydown_handlers[pg.K_RETURN] = enter

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.circle(surface, (255, 0, 0), self.cursor_pixelpos, 10) # Draw cursor as a red circle
