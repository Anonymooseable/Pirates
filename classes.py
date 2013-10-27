import collections.abc
import collections
import numbers

import circuits
from circuits.core.handlers import handler

import pygame

import draw

class Vector2 (collections.abc.Sequence):
	def __init__(self, x, y = None):
		if y is not None:
			self.x = x
			self.y = y
		else:
			self.x = x[0]
			self.y = x[1]

	def __getitem__(self, index):
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		else:
			raise IndexError("Index out of range for 2D vector")

	def __len__(self):
		return 2

	def __repr__(self):
		return "%s(%d, %d)" % (self.__class__.__name__, self.x, self.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, other):
		return tuple(other) == tuple(self)

	def int(self):
		return Vector2(int(self.x), int(self.y))

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		return Vector2(self.x * other, self.y * other)

AnimatedAttribute = collections.namedtuple("AnimatedAttribute",("begin", "end"))
aa = AnimatedAttribute

class Animator (circuits.BaseComponent):
	def __init__(self, total_time, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.time = 0.0
		self.total_time = total_time

		for key, value in kwargs.items():
			setattr(self, key, property(self._attribute_calculator(value)))

	@handler("update")
	def _on_update(self):
		if self.time < 1:
			self.time += 1/self.root.FPS / self.total_time
		else:
			self.unregister()

	def _attribute_calculator (self, attribute):
		def _attribute(self):
			return attribute.begin + (attribute.end - attribute.begin) * self.time
		return _attribute

class ColourAnimator(Animator):
	def __init__(self, total_time, c1, c2):
		super().__init__(total_time)
		self._r = AnimatedAttribute(c1.r, c2.r)
		self._g = AnimatedAttribute(c1.g, c2.g)
		self._b = AnimatedAttribute(c1.b, c2.b)
		self._a = AnimatedAttribute(c1.a, c2.a)
	def r(self):
		attribute = self._r
		return int(attribute.begin + (attribute.end - attribute.begin) * self.time)
	def g(self):
		attribute = self._g
		return int(attribute.begin + (attribute.end - attribute.begin) * self.time)
	def b(self):
		attribute = self._b
		return int(attribute.begin + (attribute.end - attribute.begin) * self.time)
	def a(self):
		attribute = self._a
		return int(attribute.begin + (attribute.end - attribute.begin) * self.time)

	def colour(self):
		return pygame.Color(self.r(), self.g(), self.b(), self.a())
