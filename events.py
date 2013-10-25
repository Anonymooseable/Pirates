import circuits

class Update (circuits.Event):
	"""Update Event"""

class KeyEvent (circuits.Event):
	"""Generic Key event"""

class KeyDown (KeyEvent):
	"""KeyDown Event"""

class KeyUp (KeyEvent):
	"""KeyUp Event"""

class QuitRequest (circuits.Event):
	"""User requested quit (pressing escape, closing window...)"""

class KeyHandler (circuits.Component):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.keydown_handlers = {}
		self.keyup_handlers = {}

	def keydown_handler(self, key):
		def register(f):
			self.keydown_handlers[key] = f
			return f
		return register

	def keyup_handler(self, key):
		def register(f):
			self.keyup_handlers[key] = f
			return f
		return register

	def key_down(self, event, pygame_event):
		if pygame_event.key in self.keydown_handlers:
			self.keydown_handlers[pygame_event.key](self)

	def key_up(self, event, pygame_event):
		if pygame_event.key in self.keyup_handlers:
			self.keyup_handlers[pygame_event.key](self)
