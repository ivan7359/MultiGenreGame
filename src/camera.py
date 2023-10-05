import pygame, config

class CameraGroup():
	def __init__(self, world, player):
		self.world = world
		self.player = player
		self.display_surface = pygame.display.get_surface()

		# camera offset for function followToHero
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		#setup camera for function 
		l = config.CAMERA_BORDERS['left']
		t = config.CAMERA_BORDERS['top']
		w = self.display_surface.get_size()[0]  - (config.CAMERA_BORDERS['left'] + config.CAMERA_BORDERS['right'])
		h = self.display_surface.get_size()[1]  - (config.CAMERA_BORDERS['top'] + config.CAMERA_BORDERS['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)
		print(l, t, w, h)

	def followToHero(self):
		self.offset.x = round(self.player.rect.centerx - self.half_w)
		self.offset.y = round(self.player.rect.centery - self.half_h)

	def windowTargetCamera(self):

		if self.player.rect.left < self.camera_rect.left:
			self.camera_rect.left = self.player.rect.left
		if self.player.rect.right > self.camera_rect.right:
			self.camera_rect.right = self.player.rect.right
		if self.player.rect.top < self.camera_rect.top:
			self.camera_rect.top = self.player.rect.top
		if self.player.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = self.player.rect.bottom

		self.offset.x = self.camera_rect.left - config.CAMERA_BORDERS['left']
		self.offset.y = self.camera_rect.top - config.CAMERA_BORDERS['top']

	def custom_draw(self):
		# self.followToHero()
		self.windowTargetCamera()
		self.world.draw(self.offset)
		self.player.draw(self.offset)