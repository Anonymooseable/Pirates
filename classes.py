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