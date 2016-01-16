"""
Copyright (C) 2014 Linus Heckemann

This file is part of Pirates.

Pirates is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pirates is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pirates.  If not, see <http://www.gnu.org/licenses/>.
"""
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
	"""
A function object that modifies a cursor.

Used to wrap a function and its inverse, to allow attempting the modification
then reversing it if the resulting cursor is bad, as well as calling the
state's update_cursor function.

Create using CursorModifier(function, reverse_function), then register as an
event handler or call directly."""
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
	"""
Superclass for any State that maintains a cursor.

Members:
cursor - an object representing the cursor. Needs x and y members, but can be
of any class.
cursor_ok - function that returns whether the currently set cursor's value is
"ok": in bounds, etc...
update_cursor - function that performs any actions necessary after modifying
the cursor, such as updating the coordinates of the visual representation of
the cursor. """
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
		self.keydown_handler(pg.K_RETURN) (self.complete)

	def cursor_ok(self):
		"""
Returns true if the currently set cursor is acceptable and False if not.

By default, checks if the cursor is within self.root.grid's extents."""
		return 0 <= self.cursor.x < self.root.grid.width and 0 <= self.cursor.y < self.root.grid.height

	def update_cursor(self): # Updates the coordinates (in pixels) of the cursor
		"""
Updates the cursor.

By default, will set the cursor_pixelpos attribute to the coordinates in
pixels of the centre of the square at the coordinates (cursor_x, cursor_y)."""
		self.cursor_pixelpos = self.root.grid.square_centre(self.cursor)

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			self.update_cursor()

	@handler("mouse_move")
	def _on_mouse_move(self, pgevent):
		mouse_pos = Vector2(pgevent.pos)
		square = self.root.grid.pixels_to_square(mouse_pos)
		if square is not None:
			x, y = square
			oldx, oldy = self.cursor.x, self.cursor.y
			def apply(state):
				state.cursor.x, state.cursor.y = (x, y)
			def unapply(state):
				state.cursor.x, state.cursor.y = oldx, oldy
			CursorModifier(apply, unapply)(self)

	@handler("mouse_down")
	def _on_mouse_down(self, pgevent):
		self.complete()

	def complete(self, *args):
		pass
