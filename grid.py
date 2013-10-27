import circuits
from circuits.core.handlers import handler

import pygame

from draw import Drawable
from colours import square_colour_visible, square_colour_hidden, background_colour, square_colour_visible_ship
from classes import Vector2

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
		return Vector2(self.border_near(value[0]), self.border_near(value[1]))
	def square_centre(self, value):
		return Vector2(self.border_middle(value[0]), self.border_middle(value[1]))
	def square_bottomright(self, value):
		return Vector2(self.border_far(value[0]), self.border_far(value[1]))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.width = kwargs["width"]
		self.height = kwargs["height"]
		self.ships = []
		self.ships_live = []
		self.border_size = 25 # Size of border from edge of window
		self.square_size = 75 # Size of each square
		self.square_margin = 20 # Size of inter-square border
		self.all_visible = True
		# (status, ship)
		# status is:
		# 0 - invisible
		# 1 - visible
		# 2 - visible, destroyed ship
		self.squares = [[(0, None) for y in range(self.height)] for x in range(self.width)]

	@handler("ship_placed")
	def _on_ship_placed(self, event, ship):
		for other_ship in self.ships:
			if ship.collides(other_ship):
				raise CollisionError()
		for square in ship.squares:
			self.squares[square.x][square.y] = (0, ship)
		ship.grid = self
		ship.register(self)
		self.ships.append(ship)
		self.ships_live.append(ship)

	@handler("square_attacked")
	def _on_square_attacked(self, square):
		square_data = self.squares[square.x][square.y]
		if square_data[0] == 0: # The square hasn't been attacked before
			self.squares[square.x][square.y] = (1, square_data[1]) # Mark the square as visible
			if square_data[1] is not None: # There's a ship there!
				self.squares[square.x][square.y] = (3, square_data[1]) # Mark the square as "damaged ship"
				square_data[1].damages += 1

	@handler("ship_destroyed")
	def _on_ship_destroyed(self, ship):
		for x, row in enumerate(self.squares):
			for y, square in enumerate(row):
				if square[1] == ship:
					self.squares[x][y] = (3, ship)
		self.ships_live.remove(ship)

	draw_channel = 0
	def draw(self, surface):
		super().draw(surface)
		surface.fill(background_colour)
		if not self.all_visible:
			for x, row in enumerate(self.squares):
				for y, square in enumerate(row):
					square_status = square[0]
					rect = pygame.Rect(
						self.border_near(x),
						self.border_near(y),
						self.square_size,
						self.square_size
					)
					if square_status == 0:
						surface.fill(square_colour_hidden, rect)
					elif square_status in (1, 2):
						surface.fill(square_colour_visible, rect)
					elif square_status == 3:
						surface.fill(square_colour_visible_ship, rect)
		else:
			for x in range(self.width):
				for y in range(self.height):
					rect = pygame.Rect(
						self.border_near(x),
						self.border_near(y),
						self.square_size,
						self.square_size
					)
					surface.fill(square_colour_visible, rect)
