import pygame
import os

FONT_SIZE = 16

class AssetManager():
    def __init__(self, path):
        self.__sounds = {}
        self.__imgs = {}
        self.__fonts = {}

        self.__result = []
        self.path = path

    def __scanFolder(self, path, fileformat):
        listdir = os.listdir(path=path)

        for entity in listdir:
            if(os.path.isdir(path + '/' + entity)):
                self.__scanFolder(path + '/' + entity, fileformat)

            if(os.path.isfile(path + '/' + entity)):
                if(entity.find(fileformat) > 0):
                    self.__result.append(path + '/' + entity)

    def __loadResources(self, type):
        if(type == 'images'):
            self.__scanFolder(self.path, '.png')
        if(type == 'sounds'):
            self.__scanFolder(self.path, '.mp3')

    def loadSounds(self):
        # pygame.mixer.music.load()
        
        self.__loadResources('sounds')

    def loadImages(self):
        self.__loadResources('images')
        
        for file in self.__result:
            tmp = file.split('/')
            name = tmp[len(tmp) - 1].split('.')[0]

            self.__imgs[name] = pygame.image.load(file)

        self.__result.clear()

        # for i in self.__imgs:
        #     print(i, '=', self.__imgs[i])

    def loadFonts(self):
        self.__fonts['UI'] = pygame.freetype.Font("media/fonts/BD_Cartoon_Shout.ttf", FONT_SIZE)
        self.__fonts['HUD'] = pygame.freetype.Font("media/fonts/joystixmonospace.ttf", FONT_SIZE)
        self.__fonts['strategy'] = pygame.freetype.Font("media/fonts/kingdomCome.TTF", FONT_SIZE)

    def getSound(self, sound):
        return self.__sounds[sound]
    
    def getImage(self, img):
        return self.__imgs[img]
    
    def getFont(self, font):
        return self.__fonts[font]
