#!/usr/bin/env python3
import pygame
from classes import Drawable

class Ship (Drawable):
	orientations = {
		"right": 0,
		"down": 1,
		"left": 2,
		"up": 3
	}

	@property
	def length(self):
		return self._length
	@length.setter
	def length(self, value):
		self._length = int(value)
		if value < 1:
			raise ValueError("Invalid length.")

	@property
	def orientation(self):
		return self._orientation
	@orientation.setter
	def orientation(self, value):
		if value in self.orientations:
			self._orientation = self.orientations[value]
		elif value in self.orientations.values():
			self._orientation = value
		else:
			raise ValueError("Invalid orientation: %s" % str(value))

	@property
	def horizontal(self):
		return self.orientation in (self.orientations["left"], self.orientations["right"])

	@property
	def vertical(self):
		return not self.horizontal

	@property
	def corner_topleft(self):
		if self.orientation in (self.orientations["down"], self.orientations["right"]):
			return self.grid.squares_to_pixels((self.x, self.y))
		elif self.orientation == self.orientations["up"]:
			return self.grid.squares_to_pixels((self.x, self.y - self.length))
		elif self.orientation == self.orientations["left"]:
			return self.grid.squares_to_pixels((self.x - self.length, self.y))

	def collides(self, other): # Collides either with another ship or a pair of coordinates
		try:
			for square in self.squares: # TODO: optimise this using comparisons instead
				if square in other.squares:
					return True
		except NameError:
			return self.onBoat(other)

	@property
	def squares(self):
		if self.orientation == self.orientations["up"]:
			return ((self.x, y) for y in range(self.y - self.length, self.y))
		elif self.orientation == self.orientations["down"]:
			return ((self.x, y) for y in range(self.y, self.y + self.length))
		elif self.orientation == self.orientations["left"]:
			return ((x, self.y) for x in range(self.x - self.length, self.x))
		elif self.orientation == self.orientations["right"]:
			return ((x, self.y) for x in range(self.x, self.x + self.length))

	def __init__(self, length = 2, x = 0, y = 0, orientation = "down"):
		self.x = int(x)
		self.y = int(y)
		self.length = int(length)
		self.damages = []
		self.orientation = orientation
		self.grid = None
		self.colour = pygame.Color(128, 128, 128, 128)

	def onBoat(self, square): # Ugly function for testing if a square belongs to the boat (should be faster than square in self.squares)
		_x, _y = square
		if self.orientation == self.orientations["up"]:
			if _x == self.x:
				if _y <= self.y and _y >= self.y - self.length:
					return (self.x)
		elif self.orientation == self.orientations["down"]:
			if _x == self.x:
				if _y >= self.y and _y <= self.y + self.length:
					return True
		elif self.orientation == self.orientations["left"]:
			if _y == self.y:
				if _x <= self.x and _x >= self.x - self.length:
					return True
		elif self.orientation == self.orientations["right"]:
			if _y == self.y:
				if _x <= self.x and _x >= self.x - self.length:
					return True
		return False

	def draw(self, surface):
		super().draw(surface)
		if self.grid == None:
			raise ValueError("No grid found!")
		else:
			x, y = self.corner_topleft
			width = self.length if self.horizontal else 1
			height = self.length if self.vertical else 1
			surface.fill(
				self.colour,
				pygame.Rect(
					x,
					y,
					width * self.grid.square_size + (width - 1) * self.grid.square_margin,
					height * self.grid.square_size + (height - 1) * self.grid.square_margin
				)
			)

	#def attack(self, _x, _y):
	#	if self.onBoat(_x, _y):
