import circuits
from classes import Drawable, Updatable
from events import KeyHandler

class State (Drawable, Updatable, KeyHandler):
	"""Generic game state."""
