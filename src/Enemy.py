import pygame
from config import *
from Entity import *

class LiteEnemy(Entity):
    def __init__(self, objSprites, publisher, state, pos= (0, 0)):
        super().__init__(objSprites, publisher, state, pos)
        
        self.health = 10
        self.damage = 20

    def clone(self, pos):
        return LiteEnemy(self.objSprites, self.publisher, self.state, pos)

class RegularEnemy(Entity):
    def __init__(self, objSprites, publisher, state, pos= (0, 0)):
        super().__init__(objSprites, publisher, state, pos)

        self.image.fill('yellow')

        self.health = 100
        self.damage = 34

    def clone(self, pos):
        return RegularEnemy(self.objSprites, self.publisher, self.state, pos)

class HeavyEnemy(Entity):
    def __init__(self, objSprites, publisher, state, pos= (0, 0)):
        super().__init__(objSprites, publisher, state, pos)

        self.image.fill('red')

        self.health = 170
        self.damage = 90

    def clone(self, pos):
        return HeavyEnemy(self.objSprites, self.publisher, self.state, pos)
    
########################################################################

class Spawner:
    def __init__(self, prototype):
        self.prototype = prototype

    def spawnAnEnemy(self, pos):
        return self.prototype.clone(pos)