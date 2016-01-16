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

class Update (circuits.Event):
	"""Update Event"""

class PygameEvent (circuits.Event):
	"""Generic pygame event"""

class KeyEvent (PygameEvent):
	"""Generic Key event"""

class KeyDown (KeyEvent):
	"""KeyDown Event"""

class KeyUp (KeyEvent):
	"""KeyUp Event"""

class MouseEvent (PygameEvent):
	"""Generic Mouse event"""

class MouseDown (MouseEvent):
	"""MouseDown Event"""

class MouseUp (MouseEvent):
	"""MouseUp Event"""

class MouseMove(MouseEvent):
	"""MouseMove Event"""

class Quit (PygameEvent):
	"""Fired when a pygame.QUIT event is fired (window closed)"""

class QuitRequest (circuits.Event):
	"""User requested quit (pressing escape, closing window...)"""

class KeyHandler (circuits.BaseComponent):
	"""
Component that will handle key events.

Contains decorators keydown_handler and keyup_handler, which can be used to
register a function as a handler for the specified key.
Example:
class SomeHandler (KeyHandler):
	def __init__(self):
		@self.keydown_handler(pygame.K_p)
		def p_pressed(self):
			print ("The P key was pressed down.")
"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.keydown_handlers = {}
		self.keyup_handlers = {}

	def keydown_handler(self, key):
		def register(fun):
			self.keydown_handlers[key] = fun
			return fun
		return register

	def keyup_handler(self, key):
		def register(fun):
			self.keyup_handlers[key] = fun
			return fun
		return register

	@handler("key_down")
	def _on_key_down(self, pygame_event):
		if pygame_event.key in self.keydown_handlers:
			self.keydown_handlers[pygame_event.key](self)

	@handler("key_up")
	def _on_key_up(self, pygame_event):
		if pygame_event.key in self.keyup_handlers:
			self.keyup_handlers[pygame_event.key](self)

class PygamePoller (circuits.core.pollers.BasePoller):
	"""Polls pygame for events and translates them into circuits events."""
	def _generate_events(self, event):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.fire(KeyDown(event))
			elif event.type == pygame.KEYUP:
				self.fire(KeyUp(event))
			elif event.type == pygame.QUIT:
				self.fire(Quit(event))
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.fire(MouseDown(event))
			elif event.type == pygame.MOUSEBUTTONUP:
				self.fire(MouseUp(event))
			elif event.type == pygame.MOUSEMOTION:
				self.fire(MouseMove(event))
			else:
				self.fire(PygameEvent(event))
