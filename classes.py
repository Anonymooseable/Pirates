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

AnimatedAttribute = collections.namedtuple("AnimatedAttribute", ("begin", "end"))
aa = AnimatedAttribute

class Animation (circuits.BaseComponent):
	def __init__(self, total_time, begin, end):
		super().__init__()
		self._time = 0.0
		self._total_time = total_time
		self.value = self.begin = begin
		self.end = end

	@handler("update")
	def _on_update(self):
		self._time += 1 / self.root.FPS / self._total_time
		if self._time < 1:
			self.value = self.begin + (self.end - self.begin) * self._time
		else:
			self.value = self.end
			self.unregister()


class ColourAnimation (circuits.BaseComponent):
	def __init__(self, total_time, c1, c2):
		super().__init__()
		self._r = Animation(total_time, c1.r, c2.r).register(self)
		self._g = Animation(total_time, c1.g, c2.g).register(self)
		self._b = Animation(total_time, c1.b, c2.b).register(self)
		self._a = Animation(total_time, c1.a, c2.a).register(self)

	@property
	def value(self):
		c = [int(i.value) for i in [self._r, self._g, self._b, self._a]]
		return pygame.Color(*c)
