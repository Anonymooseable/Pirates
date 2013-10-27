import pygame

from circuits.core.handlers import handler


from .state import State
from classes import Vector2

text_colour = pygame.Color(255, 255, 255, 255)

class GameOverState (State):
	def __init__(self, winner, attempts):
		super().__init__()
		self.winner = winner
		self.attempts = attempts

	@handler("registered")
	def _on_registered(self, component, manager):
		if component == self:
			self.font = pygame.font.Font("economica.ttf", 64)
			screen_size = Vector2(self.root.screen.get_size())
			winner_text = self.font.render("You win!", True, text_colour)
			attempts_text = self.font.render("You took %d shots." % self.attempts, True, text_colour)
			winner_pos = screen_size * 0.5 - (Vector2(winner_text.get_size()) * 0.5) - Vector2(0, 38)
			attempts_pos = screen_size * 0.5 - (Vector2(attempts_text.get_size()) * 0.5) + Vector2(0, 38)

			self.screen = pygame.Surface(screen_size, pygame.SRCALPHA, 32)
			self.screen.blit(winner_text, winner_pos)
			self.screen.blit(attempts_text, attempts_pos)

	def draw(self, surface):
		surface.blit(self.screen, Vector2(0, 0))
