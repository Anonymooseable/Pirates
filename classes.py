import collections.abc

import circuits
from circuits.core.handlers import handler

import draw

class Updatable (circuits.BaseComponent):
	@handler("update")
	def _on_update(self, event):
		pass

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