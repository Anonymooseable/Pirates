"""
Copyright (C) 2014 Linus Heckemann

This file is part of Pirates.

Pirates is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pirates is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pirates.  If not, see <http://www.gnu.org/licenses/>.
"""
import circuits
from circuits.core.handlers import handler
import pygame

class DrawChannel:
	"""Not intended for external use."""
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
	"""
Component that will respond to draw events on the right channel.

Should generally define a draw_channel (integer) in the class, which will
determine when it will be drawn in relation to other Drawables (higher channel
number = later draw)
"""
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

class draw (circuits.Event):
	"""Event fired by the DrawManager to draw the components in its subtree."""

class DrawManager (circuits.BaseComponent):
	"""Handles drawing of all Drawables registered with it."""
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
			self.fire(draw(surface), channel)
		self.fire(draw(surface), "flip")
		return

	@handler("draw", channel = "flip")
	def _on_flip(self, event, surface):
		pygame.display.flip()
