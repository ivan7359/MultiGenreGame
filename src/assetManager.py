import pygame
import os

FONT_SIZE = 16

class AssetManager():
    def __init__(self):
        self.sounds = {}
        self.imgs = {}
        self.fonts = {}

    def loadSounds(self):
        # pygame.mixer.music.load()
        pass

    def loadImages(self):
        self.imgs['platformerBackground'] = pygame.image.load(os.path.join('media/Platformer/img/Backgrounds', 'Night1_1.png'))

    def loadFonts(self):
        self.fonts['UI'] = pygame.freetype.Font("media/fonts/BD_Cartoon_Shout.ttf", FONT_SIZE)
        self.fonts['HUD'] = pygame.freetype.Font("media/fonts/joystixmonospace.ttf", FONT_SIZE)
        self.fonts['strategy'] = pygame.freetype.Font("media/fonts/kingdomCome.TTF", FONT_SIZE)

    def getSound(self, sound):
        return self.sounds[sound]
    
    def getImage(self, img):
        return self.imgs[img]
    
    def getFont(self, font):
        return self.fonts[font]
