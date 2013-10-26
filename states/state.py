import circuits
from classes import Updatable
from draw import Drawable
from events import KeyHandler

class State (Drawable, Updatable, KeyHandler):
	"""Generic game state."""