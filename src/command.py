import pygame
import config

class Command:
    def __init__(self, player):
        self.actor = player

    def execute(self):
        pass

class Run(Command):
    def __init__(self, player, dir):
        self.direction = dir
        self.actor = player

    def execute(self):
        self.actor.move(self.direction)
        print("run")

class Jump(Command):
    def __init__(self, player):
        self.actor = player

    def execute(self):
        self.actor.jump()
        print("jump")

class InputHandler:
    def __init__(self, player):
        self.W_command = Jump(player)
        self.S_command = Command(player)
        self.A_command = Run(player, -1)
        self.D_command = Run(player, 1)

    def handleInput(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_ESCAPE]:
            config.state = config.UIEnum.Pause.value

        if self.keys[pygame.K_w]:
            self.W_command.execute()
        if self.keys[pygame.K_s]:
            self.S_command.execute()
        if self.keys[pygame.K_a]:
            self.A_command.execute()
        if self.keys[pygame.K_d]:
            self.D_command.execute()
        
        # if self.keys[pygame.K_1]:
            # info = pygame.display.Info() 
            # pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)

    def changeKeys(self, prev, curr):
        pass