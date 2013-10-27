import circuits
from circuits.core.handlers import handler

import pygame
import pygame as pg

import ship
from ship import Ship
import colours
from .cursor_state import CursorState, CursorModifier
from events import KeyHandler

class ShipPlaced (circuits.Event):
	"""Fired when the placement of a ship is confirmed by the user"""

class ShipPlaceFail (circuits.Event):
	"""Fired if a ship cannot be placed because of a collision"""

class ReturnShipColour (circuits.Event):
	"""Fired after ShipPlaceFail to return the ship colour to normal"""

class PlacingShipState (CursorState):
	ConfirmClass = ShipPlaced
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cursor = Ship(length = kwargs.pop("ship_length"))

		def _rotate_right(self):
			new_orientation = (self.cursor.orientation + 1) % 4
			self.cursor.orientation = new_orientation

		def _rotate_left(self):
			new_orientation = (self.cursor.orientation - 1) % 4
			self.cursor.orientation = new_orientation

		self.keydown_handler(pg.K_LEFTBRACKET) (CursorModifier(_rotate_left, _rotate_right))
		self.keydown_handler(pg.K_RIGHTBRACKET) (CursorModifier(_rotate_right, _rotate_left))

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			self.cursor.grid = self.root.grid

	draw_channel = 3
	def draw(self, surface):
		self.cursor.draw(surface)

	def update_cursor(self):
		pass

	@handler("ship_place_fail")
	def _on_ship_place_fail(self, event):
		self.cursor.colour = ship.error_colour
		circuits.Timer(0.4, ReturnShipColour()).register(self)

	@handler("return_ship_colour")
	def _on_return_ship_colour(self, event):
		if self.cursor.colour == ship.error_colour:
			self.cursor.colour = ship.preplaced_colour

	def complete(self):
		super().complete()
		if self.cursor.position_ok():
			self.cursor.colour = colours.default_colour
			self.fire(ShipPlaced(self.cursor))
			self.unregister()
		else:
			self.fire(ShipPlaceFail())

	def cursor_ok(self):
		return self.cursor.position_in_grid()