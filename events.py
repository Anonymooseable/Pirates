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
import circuits.core.pollers
from circuits.core.handlers import handler

import pygame

class update (circuits.Event):
	"""update Event"""

class pygame_event (circuits.Event):
	"""Generic pygame event"""

class key_event (pygame_event):
	"""Generic Key event"""

class key_down (key_event):
	"""key_down Event"""

class key_up (key_event):
	"""key_up Event"""

class mouse_event (pygame_event):
	"""Generic Mouse event"""

class mouse_down (mouse_event):
	"""mouse_down Event"""

class mouse_up (mouse_event):
	"""mouse_up Event"""

class mouse_move(mouse_event):
	"""mouse_move Event"""

class quit (pygame_event):
	"""Fired when a pygame.QUIT event is fired (window closed)"""

class quit_request (circuits.Event):
	"""User requested quit (pressing escape, closing window...)"""

class KeyHandler (circuits.BaseComponent):
	"""
Component that will handle key events.

Contains decorators key_down_handler and key_up_handler, which can be used to
register a function as a handler for the specified key.
Example:
class SomeHandler (KeyHandler):
	def __init__(self):
		@self.key_down_handler(pygame.K_p)
		def p_pressed(self):
			print ("The P key was pressed down.")
"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.key_down_handlers = {}
		self.key_up_handlers = {}

	def key_down_handler(self, key):
		def register(fun):
			self.key_down_handlers[key] = fun
			return fun
		return register

	def key_up_handler(self, key):
		def register(fun):
			self.key_up_handlers[key] = fun
			return fun
		return register

	@handler("key_down")
	def _on_key_down(self, pygame_event):
		if pygame_event.key in self.key_down_handlers:
			self.key_down_handlers[pygame_event.key](self)

	@handler("key_up")
	def _on_key_up(self, pygame_event):
		if pygame_event.key in self.key_up_handlers:
			self.key_up_handlers[pygame_event.key](self)

class PygamePoller (circuits.core.pollers.BasePoller):
	"""Polls pygame for events and translates them into circuits events."""
	def _generate_events(self, event):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.fire(key_down(event))
			elif event.type == pygame.KEYUP:
				self.fire(key_up(event))
			elif event.type == pygame.QUIT:
				self.fire(quit(event))
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.fire(mouse_down(event))
			elif event.type == pygame.MOUSEBUTTONUP:
				self.fire(mouse_up(event))
			elif event.type == pygame.MOUSEMOTION:
				self.fire(mouse_move(event))
			else:
				self.fire(pygame_event(event))
