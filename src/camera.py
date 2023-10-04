import pygame

class CameraGroup():
	def __init__(self, world, player):
		self.world = world
		self.player = player
		self.display_surface = pygame.display.get_surface()
		
		# camera offset 
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

	def followToHero(self):
		self.offset.x = round(self.player.rect.centerx - self.half_w)
		self.offset.y = round(self.player.rect.centery - self.half_h)

	def custom_draw(self):
		self.followToHero()
		self.world.draw(self.offset)
		self.player.draw(self.offset)