class DrawGroup (list, Drawable):
	def draw(self, surface):
		for i in self:
			i.draw(surface)