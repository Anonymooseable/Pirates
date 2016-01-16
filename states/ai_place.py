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
import random

from circuits.core.handlers import handler

from .state import State
import ship
from classes import Vector2
from .place_ship import ShipPlaced

class AIPlacingShipsState (State):
	"A ship-placement state that places ships randomly then immediately exits."
	def __init__(self, ship_lengths, *args, **kwargs):
		"""
Creates an AIPlacingShipsState. Accepts lengths, a list of integer ship lengths to place."""
		super().__init__(*args, **kwargs)
		self.lengths = ship_lengths

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			for ship_length in self.lengths:
				generated = False
				while not generated:
					new_ship = ship.Ship()
					new_ship.grid = self.root.grid
					new_ship.length = ship_length
					new_ship.orientation = random.choice(list(ship.Ship.orientations.keys()))
					new_ship.pos = Vector2(random.randrange(new_ship.grid.width), random.randrange(new_ship.grid.height))
					generated = new_ship.position_ok()
				yield self.call(ShipPlaced(new_ship))
			self.unregister()

	draw_channel = 99
	def draw(self, surface):
		surface.fill((0, 0, 0))
