import pygame
from config import *
from player import *

M90 = 1610612736
P90 = 2684354560
P180 = M90 * 2

class Tile(pygame.sprite.Sprite):
	def __init__(self, assetMngr, pos, groups, img_path, rotation):
		super().__init__(groups)
		self.assetMngr = assetMngr

		# self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
		# self.image.fill('white')

		self.image = self.assetMngr.getImage(img_path)
		self.image = pygame.transform.rotate(self.image, rotation)
		self.rect = self.image.get_rect(topleft = pos)
		
class Level:
	def __init__(self, assetMngr):
		self.display_surface = pygame.display.get_surface()
		self.assetMngr = assetMngr
		self.levelMap = []
		self.mapNumbers = set()
		self.tilesDict = {}
		
		# sprite group setup
		self.visible_sprites = CameraGroup()
		self.active_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		self.spritesGroup = [self.visible_sprites, self.collision_sprites]

	def translitID(self, id):
		if(len(id) > 3):
			m90_local = str(int(id) - M90 - 1)
			p180_local = str(int(id) - P180 - 1)
			p90_local = str(int(id) - P90 - 1)

			if(len(m90_local) > 0 and len(m90_local) < 4):
				return [m90_local, 90]
			
			if(len(p180_local) > 0 and len(p180_local) < 4):
				return [p180_local, 180]
		
			if(len(p90_local) > 0 and len(p90_local) < 4):
				return [p90_local, -90]
			
			return ['', 0]

		else:
			return [id, 0]

	def mainParcer(self, path):
		if path.split('.')[1] == 'txt':
			logging.info("Loading .txt map")
			self.parceTXT(path)
		else:
			logging.info("Loading .tmx map")
			self.parceTMX(path)

	def parceTXT(self, path):
		with open(path, "r") as f:

			while True:
				line = f.readline()

				if not line:
					break
				
				line = line.replace('\n', '').split(',')
				self.levelMap.append(line)
				
				for i in line:
					self.mapNumbers.add(i)

		print(self.mapNumbers)

	def parceTMX(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break

# creating [id] = [image's path] dictionary
				if line.find('<tile ') != -1:
					id = line[line.find('"') + 1 : line.rfind('"')]		# get ID

					line = f.readline()									# get path of the image
					line = line[line.find('media') : len(line)]
					line = line.replace('"/>\n', '')
					line = line.split('/')[-1].split('.')[0]
					self.tilesDict[id] = line							# create dict

# creating map from the file
				line = f.readline()

				if line.find('<data ') != -1:
					while True:
						line = f.readline()

						if line.find('</data>') != -1:
							break

						line = line.replace('\n', '').split(',')

						tmp = []

						for i in range(len(line)):
							matrix = []

							mod_line = self.translitID(line[i])
							line[i] = mod_line[0]
							rotation = mod_line[1]
							
							if (len(line[i]) > 0):
								self.mapNumbers.add(line[i])

							matrix.append(line[i])
							matrix.append(rotation)

							tmp.append(matrix)
							print(matrix)

						self.levelMap.append(tmp)

	def setup_level(self, player, currentLevel, path):
		self.player = player
		self.mainParcer(path)

		if (currentLevel == LevelEnum.Strategy.value):
			self.strategyLoader()

		if (currentLevel == LevelEnum.Shooter.value):
			self.shooterLoader()

		if (currentLevel == LevelEnum.Platformer.value):
			self.platformerLoader()

	def shooterLoader(self):
		# for row_index,row in enumerate(self.matrix):
		for row_index,row in enumerate(self.levelMap):
			for col_index,col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				for currWall in range(1, 115):
					if col == str(currWall):
					# if col in ['15', '17', '99']:
						Tile(self.assetMngr, (x,y),self.spritesGroup)
					if col == '18324':
						self.player.setPos(x, y)

	def strategyLoader(self):
		for row_index, row in enumerate(self.levelMap):
			for col_index, col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE

				if col[0] in self.mapNumbers:
					Tile(self.assetMngr, (x,y), self.spritesGroup, self.tilesDict[col[0]], col[1])
				if col[0] == '0':
					self.player.setPos(x, y)

	def platformerLoader(self):
		for row_index,row in enumerate(self.levelMap):
			for col_index,col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				if col == "1":
					Tile(self.assetMngr, (x,y),self.spritesGroup)
				if col == '7':
					self.player.setPos(x, y)
				if col == "C":
					pass
					# self.player = Player((x,y),[self.visible_sprites,self.active_sprites],self.collision_sprites)

	def getGroups(self):
		return [self.visible_sprites, self.active_sprites]

	def getCollSprites(self):
		return self.collision_sprites

	def update(self, dt):
		self.active_sprites.update(dt)
		self.visible_sprites.custom_draw(self.player)

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(100, 300)

		# center camera setup 
		# self.half_w = self.display_surface.get_size()[0] // 2
		# self.half_h = self.display_surface.get_size()[1] // 2

		# camera
		cam_left = CAMERA_BORDERS['left']
		cam_top = CAMERA_BORDERS['top']
		cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
		cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])

		self.camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)

	def custom_draw(self, player):

		# get the player offset 
		# self.offset.x = player.rect.centerx - self.half_w
		# self.offset.y = player.rect.centery - self.half_h

		# getting the camera position
		if player.rect.left < self.camera_rect.left:
			self.camera_rect.left = player.rect.left
		if player.rect.right > self.camera_rect.right:
			self.camera_rect.right = player.rect.right
		if player.rect.top < self.camera_rect.top:
			self.camera_rect.top = player.rect.top
		if player.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = player.rect.bottom

		# camera offset 
		self.offset = pygame.math.Vector2(
			self.camera_rect.left - CAMERA_BORDERS['left'],
			self.camera_rect.top - CAMERA_BORDERS['top'])

		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)


'''
id = 862
863										|	(0)
863 + 1610612736 		= 1610613599	|	(-90)
863 + 2684354560        = 2684355423	|	(90)
863 + (1610612736 * 2)	= 3221226335	|	(180)
'''

'''
id = 851

852 	 								|	(0)
852 + 1610612736 = 1610613588			|	(-90)
852 + 2684354560 = 2684355412			|	(90)
852 + (1610612736 * 2) = 3221226324		|	(180)
'''

'''

1073742385



'''

'''

EXCEPTIONS
----------

2147484497
536871222
1073742388
1073742385

'''