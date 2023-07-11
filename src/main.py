import pygame
import logging

WIDTH, HEIGHT = 1280, 720

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        logging.basicConfig(level=logging.DEBUG, filename="logs/logs.log",filemode="w")
        logging.info("Game was started")
        self.clock = pygame.time.Clock()
        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.running = True
        self.speed = 300
        self.dt = 0

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.player_pos.y -= self.speed * self.dt
        if keys[pygame.K_s]:
            self.player_pos.y += self.speed * self.dt
        if keys[pygame.K_a]:
            self.player_pos.x -= self.speed * self.dt
        if keys[pygame.K_d]:
            self.player_pos.x += self.speed * self.dt

    def update(self):
        # flip() the display to put your work on screen
        pygame.display.flip()

    def render(self):
        self.screen.fill("black")
        pygame.draw.circle(self.screen, "red", self.player_pos, 30)
        
        pygame.display.update()
        
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        self.dt = self.clock.tick(60) / 1000

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()

        logging.info("Game was stopped")
        pygame.quit()

game = Game()
game.run()