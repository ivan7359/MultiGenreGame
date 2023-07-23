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

    def execute(self, isMoving):
        self.actor.move(self.direction, isMoving)
        print("run")

class Jump(Command):
    def __init__(self, player):
        self.actor = player

    def execute(self):
        self.actor.jump()
        print("jump")

class InputHandler:
    def __init__(self, player, publisher):
        self.publisher = publisher

        self.W_command = Jump(player)
        self.S_command = Command(player)
        self.A_command = Run(player, -1)
        self.D_command = Run(player, 1)

    def handleInput(self, event, controls):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.key.key_code(controls['jump']):
                self.W_command.execute()

            if event.key == pygame.key.key_code(controls['sit_down']):
                self.S_command.execute()

            if event.key == pygame.key.key_code(controls['left']):
                self.A_command.execute(True)

            if event.key == pygame.key.key_code(controls['right']):
                self.D_command.execute(True)

            
            if event.key == pygame.K_ESCAPE:
                config.state = config.UIEnum.Pause.value

        if event.type == pygame.KEYUP:
            if event.key == pygame.key.key_code(controls['sit_down']):
                self.S_command.execute(False)

            if event.key == pygame.key.key_code(controls['left']):
                self.A_command.execute(False)

            if event.key == pygame.key.key_code(controls['right']):
                self.D_command.execute(False)

