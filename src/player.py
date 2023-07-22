import pygame
from config import *

class Player(pygame.sprite.Sprite):
	def __init__(self, groups, collision_sprites):
		super().__init__(groups)
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

	def move(self, direction):
		self.direction.x = direction

	def jump(self):
		if(self.on_floor == True):
			self.direction.y = -self.jump_speed

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_d]:
			self.direction.x = 1
		if keys[pygame.K_a]:
			self.direction.x = -1

		if keys[pygame.K_w]:
			if(self.on_floor == True):
				self.direction.y = -self.jump_speed

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
				if self.direction.y < 0:
					self.rect.top = sprite.rect.bottom
					self.direction.y = 0

		if self.on_floor and self.direction.y != 0:
			self.on_floor = False

	def update(self, dt):
		# self.input()
		self.rect.x += self.direction.x * self.speed * dt
		self.horizontal_collisions()

		self.direction.y += self.gravity
		self.rect.y += self.direction.y * dt
		self.vertical_collisions()

		self.direction.x = 0
		# self.direction.y = 0