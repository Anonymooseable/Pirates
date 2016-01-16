#!/usr/bin/env python3
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

from grid import Grid
#from states.place_all_ships import PlaceAllShipsState
from states.ai_place import AIPlacingShipsState
from states.target_ships import TargetingState
from events import KeyHandler, Quit, PygamePoller, Update
from draw import DrawManager, Draw

class PiratesGame (KeyHandler):
	"""
Runs a battleships game.
"""
	FPS = 60
	def __init__(self):
		super().__init__()
		self.pygame_poller = PygamePoller().register(self)
		self.draw_manager = DrawManager().register(self)
		self.grid = Grid(width = 7, height = 7).register(self)
		self.state_queue = [AIPlacingShipsState(ship_lengths=[2, 3, 4, 4, 5]), TargetingState()]
		self.next_state()
		self.timer = circuits.Timer(1/self.FPS, Update(), persist = True).register(self)

		@self.keydown_handler(pygame.K_ESCAPE)
		def escape_pressed(self):
			self.fire(Quit())

	@handler("started")
	def _on_started(self, *args):
		pygame.init()
		self.screen = pygame.display.set_mode((self.grid.total_width, self.grid.total_height))
		pygame.display.set_caption('Yarrrr!!')

	def next_state(self):
		if self.state_queue:
			self.state = self.state_queue.pop(0)
			self.state.register(self)
		else:
			self.stop()

	@handler("update")
	def _on_update(self, *args):
		self.fire(Draw(self.screen), "draw_manager")

	@handler("quit")
	def _on_quit(self, event):
		self.stop()

	@handler("prepare_unregister")
	def _on_prepare_unregister(self, event, component): # Switches to the next state if the component unregistered was the active state
		if component == self.state:
			self.next_state()

if __name__ == "__main__":
	PiratesGame().run()
	pygame.quit()
