import pygame
from config import *
from Entity import *

class LiteEnemy(Entity):
    def __init__(self, objSprites, publisher, pos= (0, 0)):
        super().__init__(objSprites, publisher, pos)
        
        self.health = 10
        self.damage = 20

    def clone(self, pos):
        return LiteEnemy(self.objSprites, self.publisher, pos)

class RegularEnemy(Entity):
    def __init__(self, objSprites, publisher, pos= (0, 0)):
        super().__init__(objSprites, publisher, pos)

        self.image.fill('yellow')

        self.health = 100
        self.damage = 34

    def clone(self, pos):
        return RegularEnemy(self.objSprites, self.publisher, pos)

class HeavyEnemy(Entity):
    def __init__(self, objSprites, publisher, pos= (0, 0)):
        super().__init__(objSprites, publisher, pos)

        self.image.fill('red')

        self.health = 170
        self.damage = 90

    def clone(self, pos):
        return HeavyEnemy(self.objSprites, self.publisher, pos)
    
########################################################################

class Spawner:
    def __init__(self, prototype, pos):
        self.prototype = prototype
        self.pos = pos

    def spawnAnEnemy(self):
        return self.prototype.clone(self.pos)
    
class EnemiesObjectPool:
	def __init__(self):
		self.arr = []

	def append(self, obj):
		obj.id = len(self.arr)
		self.arr.append(obj)

	def getAllEnemies(self):
		return self.arr

	def getCurrentEnemies(self, _class):
		tmp = []

		for obj in self.arr:
			if (isinstance(obj, _class)):
				tmp.append(obj)

		return tmp

	def getLiteEnemies(self):
		return self.getCurrentEnemies(LiteEnemy)

	def getRegularEnemies(self):
		return self.getCurrentEnemies(RegularEnemy)

	def getHeavyEnemies(self):
		return self.getCurrentEnemies(HeavyEnemy)

	def getEnemyById(self, id):
		for obj in self.arr:
			if (obj.id == id):
				return obj
			
		return None

	def drawAllEnemies(self):
		for obj in self.arr:
			obj.draw()


