import pygame
from config import *

SOUND_PLAYING_DELAY = 30 

class Player(pygame.sprite.Sprite):
	def __init__(self, groups, collision_sprites, publisher):
		super().__init__(groups)
		self.publisher = publisher
		self.image = pygame.Surface((TILE_SIZE // 2,TILE_SIZE))
		self.image.fill('green')
		self.rect = self.image.get_rect(center = (0, 0))

		# player movement 
		self.direction = pygame.math.Vector2()
		self.speed = 12
		self.gravity = 0.8
		self.jump_speed = 16
		self.collision_sprites = collision_sprites
		self.on_floor = False
		self.countJump = 2
		self.isMoving = False
		self.movement_sound_timer = 0


	def move(self, direction, isMoving):
		self.isMoving = isMoving
		self.direction.x = direction

	def jump(self):
		if(self.on_floor == True):
			self.publisher.notify(EventsEnum.jump.value)
			self.direction.y = -self.jump_speed
			self.countJump = self.countJump - 1
		if(self.on_floor == False and self.countJump > 0):
			self.direction.y = -self.jump_speed
			self.countJump = self.countJump - 1
		
	def setPos(self, x, y):
		self.rect.x = x
		self.rect.y = y

	def horizontal_collisions(self):
		for sprite in self.collision_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.direction.x < 0: 
					self.rect.left = sprite.rect.right
				if self.direction.x > 0: 
					self.rect.right = sprite.rect.left

	def vertical_collisions(self):
		for sprite in self.collision_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.direction.y > 0:
					self.rect.bottom = sprite.rect.top
					self.direction.y = 0
					self.on_floor = True
					self.countJump = 2
				if self.direction.y < 0:
					self.rect.top = sprite.rect.bottom
					self.direction.y = 0

		if self.on_floor and self.direction.y != 0:
			self.on_floor = False

	def update(self, dt):
		if self.movement_sound_timer > 0:
			self.movement_sound_timer -= 1
	    
		if(self.isMoving == True):
			if self.movement_sound_timer == 0 and self.on_floor == True:
				self.movement_sound_timer = SOUND_PLAYING_DELAY
				self.publisher.notify(EventsEnum.movement.value)
	
			self.rect.x += self.direction.x * self.speed * dt
			self.horizontal_collisions()

		if(self.on_floor == False):
			self.direction.y += self.gravity
			self.rect.y += self.direction.y * dt
		
		self.vertical_collisions()
 