import pygame
import random

class CollisionError(Exception):
	pass

class Grid:
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

	def squares_to_pixels(self, value, centred = False, round = False): # Top left corner or centre of a square
		try:
			out = self.border_size + (self.square_size + self.square_margin) * value + (self.square_size/2 if centred else 0)
			return (int(out) if round else out)
		except TypeError:
			return [self.squares_to_pixels(component, centred, round) for component in value]

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.ships = []
		self.border_size = 25 # Size of border from edge of window
		self.square_size = 75 # Size of each square
		self.square_margin = 20 # Size of inter-square border
		self.square_colour = pygame.Color(255, 255, 255, 255)
		self.background_colour = pygame.Color(0, 0, 0, 255)

	def place_ship(self, ship):
		for other_ship in self.ships:
			if ship.collides(other_ship):
				raise CollisionError()
		ship.grid = self
		self.ships.append(ship)

	def draw(self, screen):
		screen.fill(self.background_colour)
		for x in range(self.width):
			for y in range(self.height):
				rect = pygame.Rect(
					self.squares_to_pixels(x),
					self.squares_to_pixels(y),
					self.square_size,
					self.square_size
				)
				screen.fill(self.square_colour, rect)
