import pygame
from config import *
from player import *

M90 = 1610612736
P90 = 2684354560
P180 = M90 * 2

ID_OFFSET = 986

class Layer:
	def __init__(self, path, state):
		self.path = path
		self.state = state

		self.map = []
		self.numbers = set()
		self.tilesDict = {}

	def __translitID(self, id):
		if(len(id) > 4):
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

	def loadlayer(self, desirable_layer= 0):
		if (self.state == LevelEnum.Strategy.value):
			self.loadStrategylayer(desirable_layer)
		
		if (self.state == LevelEnum.Shooter.value or  self.state == LevelEnum.Platformer.value):
			self.loadOtherLayer()

	def loadStrategylayer(self, desirable_layer):
		with open(self.path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break

				if line.find('<layer ') != -1:
					layer = int(line.split(' ')[1].split('"')[1])
					
					if(layer == desirable_layer):
						line = f.readline()

						while True:
							line = f.readline()

							if line.find('</data>') != -1:
								break

							line = line.replace('\n', '').split(',')
							tmp = []

							for i in range(len(line)):
								matrix = []

								mod_line = self.__translitID(line[i])
								line[i] = mod_line[0]
								rotation = mod_line[1]
								
								if (len(line[i]) > 0):
									self.numbers.add(line[i])

								if(layer == 1):
									matrix.append(line[i])

								if(layer == 3 or layer == 4):
									if(line[i] in self.tilesDict.keys()):
										matrix.append(line[i])
									else:
										matrix.append('0')
								
								matrix.append(rotation)
								tmp.append(matrix)

							self.map.append(tmp)
						break

			# for i in level_layer:
			# 	CriticalLogger.critical(i)

			# InfoLogger.info(' ')

	def loadOtherLayer(self):
		with open(self.path, "r") as f:
			while True:
				line = f.readline()

				if not line:
					break
				
				line = line.replace('\n', '').split(',')
				self.map.append(line)
				
				# for i in line:
				# 	self.terrainLayer[0].numbers.add(i)

class Parser:
	def __init__(self, terrain, assetMngr):
		self.terrainLayer = terrain		# ЭТО МАССИВ
		self.assetMngr = assetMngr

	def __getTerrainIDs(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break
		
				if line.find('<tileset ') != -1:
					if (line.find('firstgid=') != -1):
						id = line[line.find('firstgid=') : line.find(' name=')].split('"')[1]
						
						if(id == "1"):
							while True:
								line = f.readline()
								line = f.readline()

								if line.find("</tileset>") != -1:
									break

								id = str(int(line[line.find('"') + 1 : line.rfind('"')]))	# get ID

								line = f.readline()									# get path of the image
								line = line[line.find('media') : len(line)]
								line = line.replace('"/>\n', '')
								line = line.split('/')[-1].split('.')[0]

								image = self.assetMngr.getImage(line)
								self.terrainLayer[0].tilesDict[id] = image							# create dict

							break

		# for i in self.terrainLayer.tilesDict:
			# InfoLogger.info(i + " " + self.terrainLayer.tilesDict[i])
		
	def __getCastlesIDs(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break

				if line.find('<tileset ') != -1:
					if (line.find('firstgid=') != -1):
						id = line[line.find('firstgid=') : line.find(' name=')].split('"')[1]
						
						if(id != 1):
							self.terrainLayer[1].numbers.add(id)

							line = f.readline()
							if(line.find('<image ') != -1):
								line = line[line.find('source=') : line.find('width=')].split('"')[1]
								line = line.split('/')[-1].split('.')[0]

								image = self.assetMngr.getImage(line)
								self.terrainLayer[1].tilesDict[id] = image
		
		# for i in self.terrainLayer[1].tilesDict:
		# 	InfoLogger.info(i + " " + self.terrainLayer[1].tilesDict[i])

	def __getLandscapeIDs(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break
		
				if line.find('<tileset ') != -1:
					if line.find('name="Landscape"') != -1:
						while True:
							line = f.readline()
							line = f.readline()

							if line.find("</tileset>") != -1:
								break

							id = str(int(line[line.find('"') + 1 : line.rfind('"')]) + ID_OFFSET)	# get ID

							line = f.readline()									# get path of the image
							line = line[line.find('..') : len(line)]
							line = line.replace('"/>\n', '')
							line = line.split('/')[-1].split('.')[0]
							
							image = self.assetMngr.getImage(line)
							self.terrainLayer[2].tilesDict[id] = image
						break

		# for i in self.terrainLayer[2].tilesDict:
		# 	InfoLogger.info(i + " " + self.terrainLayer[2].tilesDict[i])

	def __getTilesFromTileset(self, path, size, scale_factor= 1):
		tileset = pygame.image.load(path).convert()
		tileset = pygame.transform.scale(tileset, (tileset.get_width() / scale_factor, tileset.get_height() / scale_factor))

		id = 1

		for y in range(size[1]):			# size[1] - height
			for x in range(size[0]):		# size[0] - width
				self.terrainLayer[0].tilesDict[str(id)] = tileset.subsurface([x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
				id += 1

		# for i in self.terrainLayer[0].tilesDict:
		# 	InfoLogger.info(str(i) + " " + str(self.terrainLayer[0].tilesDict[i]))

	def mainParcer(self, path, currentLevel):

		if path[0].split('.')[1] == 'txt':
			InfoLogger.info("Loading .txt map")
			self.parceTXT(path, currentLevel)
		else:
			InfoLogger.info("Loading .tmx map")
			self.parceTMX(path[0])

	def parceTXT(self, path, currentLevel):
		# creating [id] = [image] dictionary
		if (currentLevel == LevelEnum.Shooter.value):
			self.__getTilesFromTileset(path[1], (6, 18), 2)

		if (currentLevel == LevelEnum.Platformer.value):
			self.__getTilesFromTileset(path[1], (8, 18), 1)

		# creating map from the file
		self.terrainLayer[0].loadlayer()
		
	def parceTMX(self, path):
		# creating [id] = [image's path] dictionary
		self.__getTerrainIDs(path)
		self.__getCastlesIDs(path)
		self.__getLandscapeIDs(path)

		# creating map from the file
		self.terrainLayer[0].loadlayer(1)
		self.terrainLayer[1].loadlayer(3)
		self.terrainLayer[2].loadlayer(4)

class Tile:
	def __init__(self, assetMngr, pos, isVisible, isCol, interaction, image, rotation, scale= 1):
		self.display_surface = pygame.display.get_surface()
		self.assetMngr = assetMngr
		self.isVisible = isVisible
		self.isCol = isCol
		self.interaction = interaction

		# self.image = self.assetMngr.getImage(img_path)
		self.image = image
		self.image = pygame.transform.rotate(self.image, rotation)
		self.image = pygame.transform.scale(self.image, (self.image.get_width() / scale, self.image.get_height() / scale))
		self.rect = self.image.get_rect(topleft = pos)

	def draw(self):
		self.display_surface.blit(self.image, self.rect.topleft)

class ObjectPool:
	def __init__(self):
		self.arr = []

	def append(self, obj):
		self.arr.append(obj)

	def getArr(self):
		return self.arr

	def draw(self):
		for obj in self.arr:
			obj.draw()

	def getOptionsArr(self, isVisible, isCol, interaction):
		tmp = set()

		if (isVisible == True):
			for obj in self.arr:
				if (obj.isVisible == True):
					tmp.add(obj)

		if (isCol == True):
			for obj in self.arr:
				if (obj.isCol == True):
					tmp.add(obj)

		for obj in self.arr:
			if (obj.interaction == interaction):
				tmp.add(obj)

		return tmp

class Level:
	def __init__(self, assetMngr, isMiniMap= False):
		self.display_surface = pygame.display.get_surface()
		self.assetMngr = assetMngr
		self.isMiniMap = isMiniMap

		self.scale = 16
		self.tiles = ObjectPool()
		self.camera = Camera(self.tiles)

	def setup_level(self, player, currentLevel, path):
		self.player = player

		if (currentLevel == LevelEnum.Strategy.value):
			self.terrainLayer = [Layer(path[0], currentLevel), Layer(path[0], currentLevel), Layer(path[0], currentLevel)]

			self.parser = Parser(self.terrainLayer, self.assetMngr)
			self.parser.mainParcer(path, currentLevel)
				
			if (self.isMiniMap == True):
				self.strategyLoader(self.terrainLayer[0], self.scale)
				self.strategyLoader(self.terrainLayer[1], self.scale)
				self.strategyLoader(self.terrainLayer[2], self.scale)
			else:
				self.strategyLoader(self.terrainLayer[0])
				self.strategyLoader(self.terrainLayer[1])
				self.strategyLoader(self.terrainLayer[2])

		if (currentLevel == LevelEnum.Shooter.value):
			self.terrainLayer = [Layer(path[0], currentLevel)]
			
			self.parser = Parser(self.terrainLayer, self.assetMngr)
			self.parser.mainParcer(path, currentLevel)

			self.shooterLoader(self.terrainLayer[0])

		if (currentLevel == LevelEnum.Platformer.value):
			self.terrainLayer = [Layer(path[0], currentLevel)]
			
			self.parser = Parser(self.terrainLayer, self.assetMngr)
			self.parser.mainParcer(path, currentLevel)

			self.platformerLoader(self.terrainLayer[0])

	def strategyLoader(self, layer, scale= 1):
		for row_index, row in enumerate(layer.map):
			for col_index, col in enumerate(row):
				if(self.isMiniMap == True):
					x = ((col_index * TILE_SIZE) / scale) + WIDTH - (len(layer.map) * 2)
					y = (row_index * TILE_SIZE) / scale
				
				else:
					x = (col_index * TILE_SIZE) / scale
					y = (row_index * TILE_SIZE) / scale

				if col[0] in layer.numbers and col[0] != '0':
					self.tiles.append(Tile(self.assetMngr, (x, y), True, True, TileEnum._None.value, layer.tilesDict[col[0]], col[1], scale))
				
				if col[0] == '18324':
					self.player.setPos(x, y)

	def shooterLoader(self, layer):
		# for row_index,row in enumerate(self.matrix):
		for row_index, row in enumerate(layer.map):
			for col_index, col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				for currWall in layer.tilesDict.keys():
					if col == str(currWall):
						self.tiles.append(Tile(self.assetMngr, (x,y), True, True, TileEnum._None.value, layer.tilesDict[col[0]], 0))
					if col == '18324':
						self.player.setPos(x, y)
					
	def platformerLoader(self, layer):
		for row_index, row in enumerate(layer.map):
			for col_index, col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				for currWall in layer.tilesDict.keys():
					if col == str(currWall):
						self.tiles.append(Tile(self.assetMngr, (x,y), True, True, TileEnum._None.value, layer.tilesDict[col[0]], 0))
					if col == '18324':
						self.player.setPos(x, y)

	def getGroups(self):
		return [self.visible_sprites, self.active_sprites]

	def getCollSprites(self):
		return self.collision_sprites

	def update(self, dt):
		self.player.update(dt)
		self.camera.followPlayer(dt, self.player, self.scale, self.isMiniMap)	# Draw the map
		self.player.draw()
		
class Camera:
	def __init__(self, tiles):
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(100, 300)
		self.tiles = tiles
		self.offset_pos = pygame.math.Vector2()

		# center camera setup 
		# self.half_w = self.display_surface.get_size()[0] // 2
		# self.half_h = self.display_surface.get_size()[1] // 2

		# camera
		cam_left = CAMERA_BORDERS['left']
		cam_top = CAMERA_BORDERS['top']
		cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
		cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])

		self.camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)
		self.prev_camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)

	def followPlayer(self, dt, player, scale, isMiniMap= False):
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

		self.offset = pygame.math.Vector2(
			self.camera_rect.left - CAMERA_BORDERS['left'],
			self.camera_rect.top - CAMERA_BORDERS['top'])

		for sprite in self.tiles.getArr():
			if (isMiniMap == False):
				if(player.isMoving[0] == True):
					sprite.rect.left -= player.direction.x * player.speed * dt
				
				if(player.isMoving[1] == True):
					sprite.rect.top -= player.direction.y * player.speed * dt

			# self.offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, sprite.rect)

		# Camera rectangle for debug 
		# pygame.draw.rect(self.display_surface, (255, 0, 0), self.camera_rect, 8)