from circuits.core.handlers import handler

import pygame
import pygame as pg

from .state import State
from .place_ship import PlacingShipState
from events import KeyHandler
import ship

class PlaceAllShipsState (State):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.lengths = [2, 3, 3, 4]
		self.selected_length = 0
		self.temp_ship = ship.Ship(length = self.lengths[self.selected_length])

		@self.keydown_handler(pg.K_RETURN)
		def confirm_ship(self):
			length = self.lengths.pop(self.selected_length)
			if self.lengths: # If we have any more ships to insert afterwards
				self.root.state_queue.insert(0, self) # We add ourself to the queue as well
			self.root.state_queue.insert(0, PlacingShipState(ship_length = length)) # Add a ship placement to the top of the state queue
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