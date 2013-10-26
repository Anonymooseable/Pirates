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
		self._on_draw = handler("draw", channel = self.real_draw_channel)(_on_draw)

	def draw(self, surface):
		print (self, "got drawn")

class Draw (circuits.Event):
	"""Event fired by the DrawManager to draw the components in its subtree."""

class DrawManager (circuits.BaseComponent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.channels = set()

	@handler("registered")
	def _on_registered(self, component, manager):
		print ("DrawManager:", component, "registered with", manager)
		if isinstance(component, Drawable):
			print ("Adding draw channel:", component.draw_channel)
			self.channels.add(DrawChannel(component.draw_channel))

	@handler("draw", channel = "draw_manager")
	def _on_draw(self, event, surface):
		for channel in sorted(self.channels):
			print ("Calling draw event on channel", channel)
			self.call(Draw(surface), channel)
			self.waitEvent(Draw(), channel)
		yield self.call(Draw(surface), "final_flip")
		return

	@handler("draw", channel = "final_flip")
	def _on_flip(self, event, surface):
		print ("flipping")
		pygame.display.flip()
