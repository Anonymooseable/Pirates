#!/usr/bin/env python3

import circuits
from circuits.core.handlers import handler

import pygame
import pygame as pg

from grid import Grid
from ship import Ship
from states.place_all_ships import PlaceAllShipsState
from events import Update, KeyDown, KeyUp, KeyHandler, Quit, PygamePoller
from draw import DrawManager, Draw

class PiratesGame (KeyHandler):
	FPS = 60
	def __init__(self):
		super().__init__()
		self.pygame_poller = PygamePoller().register(self)
		self.draw_manager = DrawManager().register(self)
		self.grid = Grid(width = 6, height = 6).register(self)
		self.state_queue = [PlaceAllShipsState()]
		self.next_state()
		self.timer = circuits.Timer(1/self.FPS, Update(), persist = True).register(self)

		@self.keydown_handler(pg.K_ESCAPE)
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
