import pygame
from config import *

class Player(pygame.sprite.Sprite):
	def __init__(self, world, publisher):
		# super().__init__(groups)
		self.display_surface = pygame.display.get_surface()
		self.world = world
		self.publisher = publisher
		self.image = pygame.Surface((TILE_SIZE // 2,TILE_SIZE))
		self.image.fill('green')
		self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
		self.coord_offset = pygame.math.Vector2()

		self.health = 100
		self.damage = 34

		# player movement 
		self.direction = pygame.math.Vector2()
		self.speed = 12
		self.gravity = 0.8
		self.jump_speed = 16
		self.on_floor = False
		self.countJump = 2
		self.isMoving = [False, False]
		self.movement_sound_timer = 0

	def horizontalMovement(self, direction, isMoving):
		self.isMoving[0] = isMoving
		self.direction.x = direction

	def verticalMovement(self, direction, isMoving):
		self.isMoving[1] = isMoving
		self.direction.y = direction

		if(currentLevel == LevelEnum.Platformer.value):
			if(self.on_floor == True):
				self.publisher.notify(EventsEnum.jump.value)
				# self.countJump = self.countJump - 1
			
			# if(self.on_floor == False and self.countJump > 0):
			# 	# self.direction.y = -self.jump_speed
			# 	self.countJump = self.countJump - 1
		
		if(currentLevel == LevelEnum.Strategy.value):
			self.direction.y = direction

	def setPos(self, x, y):
		self.coord_offset.x = x
		self.coord_offset.y = y

	def collision(self, position):
		for sprite in self.world.getArr():
			if sprite.rect.colliderect(self.rect):

				#Horizont
				if position =='x':
					if self.direction.x > 0: 
						self.rect.right = sprite.rect.left
						print("pravo")
					if self.direction.x < 0: 
						self.rect.left = sprite.rect.right
						print("levo")

				#Vertical
				if position =='y':
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top
						self.direction.y = 0
						# (print("niz"))
					if self.direction.y < 0:
						self.rect.top = sprite.rect.bottom
						self.direction.y = 0
						print("verx")

	def move(self, dt):
		self.on_floor = False
		# horizontal movement
		if(self.isMoving[0] == True):
			self.rect.x += self.direction.x * self.speed * dt
			self.collision('x')

		# vertical movement
		if(self.isMoving[1] == True):
			self.on_floor = True
			self.rect.y += self.direction.y * self.jump_speed * dt
			self.collision('y')
			print("rect.y: ", self.rect.y)

	def update(self, dt):
		# if self.movement_sound_timer > 0:
		# 	self.movement_sound_timer -= 1
	    
		# if(self.isMoving[0] == True):
		# 	if self.movement_sound_timer == 0 and self.on_floor == True:
		# 		self.movement_sound_timer = SOUND_PLAYING_DELAY
		# 		self.publisher.notify(EventsEnum.movement.value)
	
			# self.rect.x += self.direction.x * self.speed * dt
			# self.horizontal_collisions()
		
		if(currentLevel == LevelEnum.Platformer.value):
			# Если герой не на земле
			if(self.on_floor != True and self.isMoving[1] == False):
				self.direction.y += self.gravity
				self.rect.y += self.direction.y * dt
				self.on_floor = True # Позволяет всегда проверять что герой не прилип к земле
				if(self.isMoving[1] != True):
					self.collision('y')

			# self.apply_gravity(dt)
			self.move(dt)
			# self.checkOnFloor()
		# self.horizontal_movement_collision()
		# self.get_player_on_ground()
		# self.vertical_movement_collision(dt)

		if(currentLevel == LevelEnum.Strategy.value):
			# if(self.isMoving[1] == True):
			# 	self.rect.y += self.direction.y * self.speed * dt
			pass

	def draw(self):
		self.display_surface.blit(self.image, self.rect.topleft)