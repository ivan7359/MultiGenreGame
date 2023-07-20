import pygame

from observer import *
from command import *
from assetManager import *
from config import *

from player import *
from level import *

class GameState():
    def __init__(self, pos):
        self.x = pos.x
        self.y = pos.y

    def update(self, moveCommandX, moveCommandY):
        self.x += moveCommandX
        self.y += moveCommandY

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        logging.info("Game was started")

# Load all resources
        self.assetMngr = AssetManager('media')
        # self.assetMngr.loadImages()
        # self.assetMngr.loadSounds()
        # self.assetMngr.loadFonts()

        self.gameState = GameState(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.publisher = Subject()
        self.publisher.addObserver(Audio())
        self.inputHandler = InputHandler(self.screen)

        self.level = Level()
        self.player = Player(self.level.getGroups(), self.level.getCollSprites())
        self.level.setup_level(self.player)

        self.running = True
        self.speed = 7
        self.dt = 0                 # delta time in seconds since last frame

        self.moveCommandX = 0
        self.moveCommandY = 0 

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def processInput(self):
        self.moveCommandX = 0
        self.moveCommandY = 0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            
        # command = self.inputHandler.handleInput()
        # if(command):
        #     command.execute()

    def update(self):
        # We delegate store and update game data to GameState class
        self.gameState.update(self.moveCommandX, self.moveCommandY)
        self.level.update()

    def render(self):
        # pygame.draw.circle(self.screen, "red", (self.gameState.x, self.gameState.y), 30)
        
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()

            self.dt = self.clock.tick(FPS) / SPEED_SCALE

        logging.info("Game was stopped")
        pygame.quit()

game = Game()
game.run()