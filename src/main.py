import pygame
import logging

WIDTH, HEIGHT = 1280, 720
FPS = 60                        # limits FPS to 60
SPEED_SCALE = 30

class GameState():
    def __init__(self, pos):
        self.x = pos.x
        self.y = pos.y

    def update(self, moveCommandX, moveCommandY):
        self.x += moveCommandX
        self.y += moveCommandY

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        logging.basicConfig(level=logging.DEBUG, filename="logs/logs.log",filemode="w")
        logging.info("Game was started")
        self.clock = pygame.time.Clock()
        self.gameState = GameState(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2))

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

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.moveCommandY -= self.speed * self.dt
        if keys[pygame.K_s]:
            self.moveCommandY += self.speed * self.dt
        if keys[pygame.K_a]:
            self.moveCommandX -= self.speed * self.dt
        if keys[pygame.K_d]:
            self.moveCommandX += self.speed * self.dt

    def update(self):
        # We delegate store and update game data to GameState class
        self.gameState.update(self.moveCommandX, self.moveCommandY)

    def render(self):
        self.screen.fill("black")
        pygame.draw.circle(self.screen, "red", (self.gameState.x, self.gameState.y), 30)
        
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