class CollisionError(Exception):
	pass

class Grid:
	@property
	def total_width(self):
	    return self.border_size * 2	+ self.width * self.square_size + (self.width-1) * self.square_margin
	@property
	def total_height(self):
	    return self.border_size * 2	+ self.height * self.square_size + (self.height-1) * self.square_margin
	
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.ships = []
		self.border_size = 25 # Size of border from edge of window
		self.square_size = 75 # Size of each square
		self.square_margin = 20 # Size of inter-square border
		self.square_colour = pygame.Color(255, 255, 255, 255)
		self.background_colour = pygame.Color(0, 0, 0, 255)

	def place_ship(self, ship):
		for other_ship in self.ships:
			if ship.collides(other_ship):
				raise CollisionError()
		ship.grid = self
		self.ships.append(ship)

	def draw(self, screen):
		screen.fill(self.background_colour)
		for x in range(width):
			for y in range(height):
				rect = pygame.Rect(
					self.square_size,
					self.square_size,
					self.border_size + (self.square_size + self.square_margin) * x,
					self.border_size + (self.square_size + self.square_margin) * y,
				)
				screen.fill(self.square_colour, rect)
