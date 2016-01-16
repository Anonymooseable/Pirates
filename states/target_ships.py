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

from .cursor_state import CursorState, CursorModifier
from .game_over import GameOverState
from events import KeyHandler

class SquareAttacked (circuits.Event):
	"""Fired when a player fires at a position in the grid"""

class TargetingState (CursorState):
	"""
Main in-game state, where a player aims and fires at squares.

Receives input from player, selecting squares using the mouse or keyboard to
try and find and sink the enemy's ships. Exits and passes on to a GameOverState
when all the ships have been sunk.
"""
	def update_cursor(self):
		super().update_cursor()
		self.cursor_pixelpos = self.root.grid.square_centre(self.cursor).int()

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			self.root.grid.all_visible = False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.attempts = 0

	draw_channel = 3
	def draw(self, surface):
		super().draw(surface)
		# Draw cursor as a red circle
		pygame.draw.circle(surface, (255, 0, 0), self.cursor_pixelpos, 5)

	@handler("square_attacked")
	def _on_square_attacked(self, square):
		self.attempts += 1

	@handler("ship_destroyed")
	def _on_ship_destroyed(self, ship):
		if (
				len(self.root.grid.ships_live) <= 1 and
				ship in self.root.grid.ships_live
			) or len(self.root.grid.ships_live) == 0:
			self.root.state_queue.append(GameOverState("", self.attempts))
			self.unregister()

	def complete(self, *args):
		self.fire(SquareAttacked(self.cursor))
