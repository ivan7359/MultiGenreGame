import pygame
import os

from config import *

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
        logging.info("LOADING SOUNDS")
        self.__loadResources('sounds')

        for file in self.__result:
            tmp = file.split('/')
            name = tmp[len(tmp) - 1].split('.')[0]
            self.__sounds[name] = pygame.mixer.Sound(file)

        self.__result.clear()

        for i in self.__sounds:
            logging.debug(i + ' = ' + str(self.__sounds[i]))

    def loadImages(self):
        logging.info("LOADING IMAGES")
        self.__loadResources('images')
        
        for file in self.__result:
            tmp = file.split('/')
            name = tmp[len(tmp) - 1].split('.')[0]
            self.__imgs[name] = pygame.image.load(file)

        self.__result.clear()

        for i in self.__imgs:
            logging.debug(i + ' = ' + str(self.__imgs[i]))

    def loadFonts(self):
        logging.info("LOADING FONTS")

        self.__fonts['UI'] = pygame.freetype.Font("media/fonts/BD_Cartoon_Shout.ttf", FONT_SIZE)
        self.__fonts['HUD'] = pygame.freetype.Font("media/fonts/joystixmonospace.ttf", FONT_SIZE)
        self.__fonts['strategy'] = pygame.freetype.Font("media/fonts/kingdomCome.TTF", FONT_SIZE)

        for i in self.__fonts:
            logging.debug(i + ' = ' + str(self.__fonts[i]))

    def getSound(self, sound):
        return self.__sounds[sound]
    
    def getImage(self, img):
        return self.__imgs[img]
    
    def getFont(self, font):
        return self.__fonts[font]
