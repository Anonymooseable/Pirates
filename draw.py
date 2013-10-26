import circuits
from circuits.core.handlers import handler
import pygame

class DrawChannel:
	def __setattr__(self, attr, value):
		raise TypeError("DrawChannel is immutable")

	def __init__(self, index):
		super().__setattr__("index", index)
		super().__setattr__("hash", hash(index))

	def __hash__(self):
		return self.hash

	def __lt__(self, other):
		return self.index < other.index

	def __repr__(self):
		return "%s %d" % (self.__class__.__name__, self.index)

class Drawable (circuits.BaseComponent):
	draw_channel = 50
	real_draw_channel = None
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		def _on_draw(self, surface):
			return self.draw(surface)
		self.real_draw_channel = DrawChannel(self.draw_channel)
		draw = handler("draw", channel = self.real_draw_channel)(_on_draw)
		self.addHandler(draw)

	def draw(self, surface):
		pass

class Draw (circuits.Event):
	"""Event fired by the DrawManager to draw the components in its subtree."""

class DrawManager (circuits.BaseComponent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.channels = set()

	@handler("registered")
	def _on_registered(self, component, manager):
		if isinstance(component, Drawable):
			self.channels.add(component.real_draw_channel)

	@handler("draw", channel = "draw_manager")
	def _on_draw(self, event, surface):
		for channel in sorted(self.channels):
			self.fire(Draw(surface), channel)
		self.fire(Draw(surface), "flip")
		return

	@handler("draw", channel = "flip")
	def _on_flip(self, event, surface):
		pygame.display.flip()
