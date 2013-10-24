import circuits
import pygame
import pygame as pg

import grid
from .state import State
from util import clamp
from classes import Vector2

from events import KeyHandler

class CursorState (State):
	def __init__(self):
		super().__init__()
		self.cursor = Vector2(0, 0)

	def cursor_ok(self):
		"""Returns true if the currently set cursor is acceptable and False if not.

By default, checks if the cursor is within self.root.grid's extents."""
		return 0 <= self.cursor.x < self.root.grid.width and 0 <= self.cursor.y < self.root.grid.height

	def update_cursor(self): # Updates the coordinates (in pixels) of the cursor
		"""Updates the cursor.

By default, will set the cursor_pixelpos attribute to the coordinates in pixels of the centre of the square at the coordinates (cursor_x, cursor_y)."""
		self.cursor_pixelpos = self.root.grid.square_centre(self.cursor)

	def registered(self, *args):
		self.update_cursor()

	def cursor_modifier(reverse_fun): # Decorator for functions that move the cursor
		"""Wraps a function that will modify the cursor.

This decorator will first check if the new cursor value is acceptable by referring to cursor_ok(), then reset it if not.
If the new value is acceptable, it will call update_cursor() to take the changes into account."""
		def wrap(fun):
			def result(self, *args):
				fun(self, *args)
				if not self.cursor_ok():
					reverse_fun(self)
				else:
					self.update_cursor()
			return result
		return wrap

	def _up(self):
		self.cursor.y -= 1
	def _down(self):
		self.cursor.y += 1
	def _left(self):
		self.cursor.x -= 1
	def _right(self):
		self.cursor.x += 1

	left = KeyHandler.keydown_handler(pg.K_LEFT)(cursor_modifier(_right)(_left))
	right = KeyHandler.keydown_handler(pg.K_RIGHT)(cursor_modifier(_left)(_right))
	up = KeyHandler.keydown_handler(pg.K_UP)(cursor_modifier(_down)(_up))
	down = KeyHandler.keydown_handler(pg.K_DOWN)(cursor_modifier(_up)(_down))