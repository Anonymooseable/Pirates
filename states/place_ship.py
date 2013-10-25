import circuits
import pygame
import pygame as pg

import ship
from ship import Ship
from .cursor_state import CursorState
from events import KeyHandler
from classes import Drawable

class ShipPlaced (circuits.Event):
	"""Fired when the placement of a ship is confirmed by the user"""

class ShipPlaceFail (circuits.Event):
	"""Fired if a ship cannot be placed because of a collision"""

class ReturnShipColour (circuits.Event):
	"""Fired after ShipPlaceFail to return the ship colour to normal"""

class PlacingShipState (CursorState):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cursor = Ship(length = kwargs.pop("ship_length"))

		@self.keydown_handler(pg.K_RETURN)
		def confirm(self):
			if self.cursor.position_ok():
				self.cursor.colour = ship.default_colour
				self.fire(ShipPlaced(self.cursor))
				self.unregister()
			else:
				self.fire(ShipPlaceFail())

		def _rotate_right(self):
			new_orientation = (self.cursor.orientation + 1) % 4
			self.cursor.orientation = new_orientation

		def _rotate_left(self):
			new_orientation = (self.cursor.orientation - 1) % 4
			self.cursor.orientation = new_orientation
		rotate_right = self.keydown_handler(pg.K_RIGHTBRACKET)(self.cursor_modifier(_rotate_left)(_rotate_right))
		rotate_left = self.keydown_handler(pg.K_LEFTBRACKET)(self.cursor_modifier(_rotate_right)(_rotate_left))

	def registered(self, *args):
		self.cursor.grid = self.root.grid

	def draw(self, surface):
		super().draw(surface)
		self.cursor.draw(surface)

	def update_cursor(self):
		pass

	def ship_place_fail(self, event):
		self.cursor.colour = ship.error_colour
		circuits.Timer(0.4, ReturnShipColour()).register(self)

	def return_ship_colour(self, event):
		if self.cursor.colour == ship.error_colour:
			self.cursor.colour = ship.preplaced_colour

	def cursor_ok(self):
		return self.cursor.position_in_grid()