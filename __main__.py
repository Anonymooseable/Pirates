#!/usr/bin/env python3

import circuits

import pygame
import pygame as pg

from grid import Grid
from ship import Ship
from states import select_square, place_ship
from events import Update, KeyDown, KeyUp, QuitRequest
from classes import DrawGroup

class PiratesGame (circuits.Component):
	FPS = 60
	def __init__(self):
		super().__init__()
		self.grid = Grid(6, 6).register(self)
		self.state = place_ship.PlacingShipState(2).register(self)
		self.timer = circuits.Timer(1/self.FPS, Update(), persist = True).register(self)

		self.draw_queue = {0: self.grid, 10: self.state}

	def started(self, *args):
		pygame.init()
		self.screen = pygame.display.set_mode((self.grid.total_width, self.grid.total_height))
		pygame.display.set_caption('Yarrrr!!')

	def update(self, *args):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				e = KeyDown(event)
				self.fire(e)
			elif event.type == pygame.QUIT:
				self.fire(QuitRequest())
		self.draw()

	def draw(self):
		for key in sorted(self.draw_queue):
			self.draw_queue[key].draw(self.screen)
		pygame.display.flip()

	def key_down(self, event, pygame_event):
		if pygame_event.key == pg.K_ESCAPE:
			self.fire(QuitRequest())

	def quit_request(self):
		self.stop()

	def prepare_unregister(self, event, component): # Removes an item from the draw queue if it gets unregistered
		pop_keys = []
		for key, value in self.draw_queue.items():
			if isinstance(value, circuits.Component) and event.in_subtree(value):
				pop_keys.append(key)
		for key in pop_keys:
			self.draw_queue.pop(key)

	def ship_placed(self, event, ship):
		self.state = place_ship.PlacingShipState(3).register(self)
		self.draw_queue[10] = self.state

if __name__ == "__main__":
	PiratesGame().run()
