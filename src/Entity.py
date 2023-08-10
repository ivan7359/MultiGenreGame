import pygame
from config import *

class Entity:
    def __init__(self, objSprites, publisher, state, pos= (0, 0)):
        self.display_surface = pygame.display.get_surface()
        self.objSprites = objSprites
        self.publisher = publisher
        self.state = state

        self.life = True
        # self.health = 100
        # self.damage = 30

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)

        self.speed = 8
        self.direction = pygame.math.Vector2()
        self.isMoving = [False, False]

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def clone(self):
        pass

    def draw(self):
        self.display_surface.blit(self.image, self.rect.topleft)

