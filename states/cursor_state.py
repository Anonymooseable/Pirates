import circuits
from circuits.core.handlers import handler

import pygame
import pygame as pg

import grid
from .state import State
from util import clamp
from classes import Vector2
from events import KeyHandler

class CursorModifier:
	def __init__(self, do_modification, reverse_modification):
		self.do_modification = do_modification
		self.reverse_modification = reverse_modification

	def __call__(self, state):
		self.do_modification(state)
		if not state.cursor_ok():
			self.reverse_modification(state)
		else:
			state.update_cursor()

class CursorState (State, KeyHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cursor = Vector2(0, 0)

		def _up(self):
			self.cursor.y -= 1
		def _down(self):
			self.cursor.y += 1
		def _left(self):
			self.cursor.x -= 1
		def _right(self):
			self.cursor.x += 1

		self.keydown_handler(pg.K_LEFT) (CursorModifier(_left, _right))
		self.keydown_handler(pg.K_RIGHT) (CursorModifier(_right, _left))
		self.keydown_handler(pg.K_UP) (CursorModifier(_up, _down))
		self.keydown_handler(pg.K_DOWN) (CursorModifier(_down, _up))

	def cursor_ok(self):
		"""Returns true if the currently set cursor is acceptable and False if not.

By default, checks if the cursor is within self.root.grid's extents."""
		return 0 <= self.cursor.x < self.root.grid.width and 0 <= self.cursor.y < self.root.grid.height

	def update_cursor(self): # Updates the coordinates (in pixels) of the cursor
		"""Updates the cursor.

By default, will set the cursor_pixelpos attribute to the coordinates in pixels of the centre of the square at the coordinates (cursor_x, cursor_y)."""
		self.cursor_pixelpos = self.root.grid.square_centre(self.cursor)

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			self.update_cursor()
