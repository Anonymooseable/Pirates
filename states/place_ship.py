import circuits
import pygame
import pygame as pg

from ship import Ship
from .cursor_state import CursorState

class ShipPlaced (circuits.Event):
    """Fired when the placement of a ship is confirmed by the user"""
    def __init__(self, selection):
        super().__init__()
        self.selection = selection

class PlacingShipState (CursorState):
    def __init__(self, shipLength):
        super().__init__()
        self.ship = Ship()
        def enter(self):
            self.fire(ShipPlaced(self.ship))
            self.unregister()
        def rotate_right(self):
            new_orientation = (self.ship.orientation + 1) % 4
            self.ship.orientation = new_orientation
        def rotate_left(self):
            new_orientation = (self.ship.orientation - 1) % 4
            self.ship.orientation = new_orientation

        self.keydown_handlers.update({
            pg.K_RETURN: enter,
            pg.K_LEFTBRACKET: rotate_left,
            pg.K_RIGHTBRACKET: rotate_right
        })

    def registered(self, *args):
        self.ship.grid = self.root.grid

    def draw(self, surface):
        super().draw(surface)
        self.ship.draw(surface)

    def update_cursor(self):
        self.ship.x, self.ship.y = self.cursor_x, self.cursor_y
