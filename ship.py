#!/usr/bin/env python3
import pygame

import circuits
from circuits.core.handlers import handler

from classes import Vector2, ColourAnimator
from draw import Drawable

from colours import default_colour, preplaced_colour, prepicked_colour, error_colour, destroyed_colour

class ShipDestroyed (circuits.Event):
	"""Fired by a ship when it gets destroyed."""

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
			return (self.x, self.y)
		elif self.orientation == self.orientations["up"]:
			return (self.x, self.y - self.length + 1)
		elif self.orientation == self.orientations["left"]:
			return (self.x - self.length + 1, self.y)

	@property
	def corner_bottomright(self):
		if self.orientation in (self.orientations["up"], self.orientations["left"]):
			return self.pos
		elif self.orientation == self.orientations["down"]:
			return Vector2(self.x, self.y + self.length - 1)
		elif self.orientation == self.orientations["right"]:
			return Vector2(self.x + self.length - 1, self.y)

	def collides(self, other): # Collides either with another ship or a pair of coordinates
		try:
			for square in self.squares: # TODO: optimise this using comparisons instead
				if square in other.squares:
					return True
			return False
		except NameError:
			return self.onBoat(other)

	@property
	def x(self):
		return self.pos.x
	@x.setter
	def x(self, value):
		self.pos.x = value

	@property
	def y(self):
		return self.pos.y
	@y.setter
	def y(self, value):
		self.pos.y = value

	@property
	def squares(self):
		if self.orientation == self.orientations["up"]:
			return (Vector2(self.x, y + 1) for y in range(self.y - self.length, self.y))
		elif self.orientation == self.orientations["down"]:
			return (Vector2(self.x, y) for y in range(self.y, self.y + self.length))
		elif self.orientation == self.orientations["left"]:
			return (Vector2(x + 1, self.y) for x in range(self.x - self.length, self.x))
		elif self.orientation == self.orientations["right"]:
			return (Vector2(x, self.y) for x in range(self.x, self.x + self.length))

	@property
	def damages(self):
		return self._damages
	@damages.setter
	def damages(self, value):
		self._damages = value
		if self._damages >= self.length:
			self.fire(ShipDestroyed(self))
			self.colour = ColourAnimator(4.0, self.colour, destroyed_colour).register(self)
			self.destroyed = True

	def __init__(self, length = 2, x = 0, y = 0, orientation = "down", *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.pos = Vector2(x, y)
		self.length = int(length)
		self.damages = 0
		self.orientation = orientation
		self.grid = None
		self.colour = preplaced_colour
		self.destroyed = False

	def onBoat(self, square): # Ugly function for testing if a square belongs to the boat (should be faster than square in self.squares)
		_x, _y = square
		if self.orientation == self.orientations["up"]:
			if _x == self.x:
				if _y <= self.y and _y >= self.y - self.length:
					return True
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

	draw_channel = 1
	def draw(self, surface):
		super().draw(surface)
		if self.grid == None:
			raise ValueError("No grid found!")
		elif self.grid.all_visible or self.destroyed:
			top_left = self.grid.square_topleft(self.corner_topleft)
			bottom_right = self.grid.square_bottomright(self.corner_bottomright)

			margin = self.grid.square_size / 7
			top_left += Vector2(margin, margin)
			bottom_right -= Vector2(margin, margin)

			size = bottom_right - top_left

			sprite = pygame.Surface(size, pygame.SRCALPHA, 32)
			try:
				sprite.fill(self.colour.colour())
				#sprite.set_alpha(self.colour.a)
			except AttributeError:
				sprite.fill(self.colour)
			surface.blit(sprite, top_left)

	def position_in_grid(self):
		x, y = self.corner_topleft
		if x < 0 or y < 0:
			return False
		x, y = self.corner_bottomright
		if x > self.grid.width - 1 or y > self.grid.height - 1:
			return False
		return True

	def position_ok(self):
		if not self.position_in_grid():
			return False
		for other in self.grid.ships:
			if self.collides(other):
				return False
		return True