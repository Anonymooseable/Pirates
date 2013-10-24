import circuits

class Drawable:
	def draw(self, surface):
		pass

class Updatable (circuits.Component):
	def update(self, event):
		pass

class DrawGroup (list, Drawable):
	def draw(self, surface):
		for i in self:
			i.draw(surface)

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __list__(self):
		return [self.x, self.y]

	def __tuple__(self):
		retrun (self.x, self.y)