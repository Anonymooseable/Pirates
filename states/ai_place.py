import random

from circuits.core.handlers import handler

from .state import State
import ship
from classes import Vector2
from .place_ship import ShipPlaced

class AIPlacingShipsState (State):
	@handler("registered")
	def _on_registered(self, component, manager):
		if (component == self):
			for ship_length in [2, 3, 3, 4]:
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