#!/usr/bin/env python3

class Ship:
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
		

	def __init__(self, length, x, y, orientation):
		self.x = int(x)
		self.y = int(y)
		self.length = int(length)
		self.damages = []
		if orientation in self.orientations.keys():
			self.orientation = self.orientations[orientation]
		elif orientation in self.orientations.values():
			self.orientation = orientation
		else:
			raise ValueError("Invalid orientation: %s" % str(orientation))

	def onBoat(self, _x, _y):
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
					return 
		return False

	#def attack(self, _x, _y):
	#	if self.onBoat(_x, _y):
