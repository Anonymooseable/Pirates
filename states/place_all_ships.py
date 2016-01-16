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
from circuits.core.handlers import handler

import pygame
import pygame as pg

from .state import State
from .place_ship import PlacingShipState
from events import KeyHandler
import ship

class PlaceAllShipsState (State, KeyHandler):
	"""
State for getting a user to place ships.

Allows the user to select from a list of ships, then delegates the task of
placing the ships to PlacingShipStates. Repeats for all the ships provided
to its constructor.
"""
	def __init__(self, ship_lengths, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.lengths = ship_lengths
		self.selected_length = 0
		self.temp_ship = ship.Ship(length = self.lengths[self.selected_length])

		@self.keydown_handler(pg.K_RETURN)
		def confirm_ship(self):
			length = self.lengths.pop(self.selected_length)
			if self.lengths: # If we have any more ships to insert afterwards
				self.root.state_queue.insert(0, self) # We add ourself to the queue as well
			# Add a ship placement to the top of the state queue
			self.root.state_queue.insert(0, PlacingShipState(ship_length = length))
			self.unregister() # And pass on to it by unregistering ourselves

		@self.keydown_handler(pg.K_PLUS)
		@self.keydown_handler(pg.K_EQUALS)
		def increase_length(self):
			self.selected_length += 1
			self.selected_length %= len(self.lengths)
			self.temp_ship.length = self.lengths[self.selected_length]

		@self.keydown_handler(pg.K_MINUS)
		def decrease_length(self):
			self.selected_length -= 1
			self.selected_length %= len(self.lengths)
			self.temp_ship.length = self.lengths[self.selected_length]

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			self.temp_ship.grid = self.root.grid
			self.selected_length %= len(self.lengths)
			self.temp_ship.length = self.lengths[self.selected_length]
			self.temp_ship.colour = ship.prepicked_colour
			self.root.grid.all_visible = True

	draw_channel = 3
	def draw(self, surface):
		super().draw(surface)
		self.temp_ship.draw(surface)
