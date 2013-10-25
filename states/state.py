import circuits
from classes import Drawable, Updatable
from events import KeyHandler

class State (Drawable, Updatable, KeyHandler):
	"""Generic game state."""
	def __init__(self, *args, **kwargs):
		return_to = kwargs.pop("return_to", None)
		super().__init__(*args, **kwargs)
		if return_to:
			def prepare_unregister(self, *args):
				super().prepare_unregister(*args)
				return_to.register(self.parent)
			self.prepare_unregister = prepare_unregister