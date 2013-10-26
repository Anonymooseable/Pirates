import circuits
from circuits.core.handlers import handler

import pygame

from draw import Drawable

class CollisionError(Exception):
	pass

class Grid (Drawable):
	@property
	def total_width(self):
		return self.border_size * 2	+ self.width * self.square_size + (self.width-1) * self.square_margin
	@property
	def total_height(self):
		return self.border_size * 2	+ self.height * self.square_size + (self.height-1) * self.square_margin

	def pixels_to_squares(self, value):
		try:
			return (value - self.border_size) // (self.square_size + self.square_margin)
		except TypeError:
			return [self.pixels_to_squares(component) for component in value]

	def border_near(self, value):
		return (self.border_size + (self.square_size + self.square_margin) * value)
	def border_far(self, value):
		return (self.border_size + (self.square_size + self.square_margin) * value) + self.square_size
	def border_middle(self, value):
		return (self.border_size + (self.square_size + self.square_margin) * value) + self.square_size / 2

	def square_topleft(self, value):
		return (self.border_near(value[0])), self.border_near(value[1])
	def square_centre(self, value):
		return (self.border_middle(value[0]), self.border_middle(value[1]))
	def square_bottomright(self, value):
		return (self.border_far(value[0]), self.border_far(value[1]))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.width = kwargs["width"]
		self.height = kwargs["height"]
		self.ships = []
		self.border_size = 25 # Size of border from edge of window
		self.square_size = 75 # Size of each square
		self.square_margin = 20 # Size of inter-square border
		self.square_colour = pygame.Color(255, 255, 255, 255)
		self.background_colour = pygame.Color(0, 0, 0, 255)

	@handler("ship_placed")
	def _on_ship_placed(self, event, ship):
		for other_ship in self.ships:
			if ship.collides(other_ship):
				raise CollisionError()
		ship.grid = self
		ship.register(self)
		self.ships.append(ship)

	draw_channel = 0
	def draw(self, surface):
		super().draw(surface)
		surface.fill(self.background_colour)
		for x in range(self.width):
			for y in range(self.height):
				rect = pygame.Rect(
					self.border_near(x),
					self.border_near(y),
					self.square_size,
					self.square_size
				)
				surface.fill(self.square_colour, rect)
