import pygame
import config

class Command:
    def __init__(self, player, dir):
        self.direction = dir
        self.actor = player

    def execute(self):
        pass

class HorizontalMovement(Command):
    def __init__(self, player, dir):
        super().__init__(player, dir)

    def execute(self, isMoving):
        self.actor.horizontalMovement(self.direction, isMoving)

class VerticalMovement(Command):
    def __init__(self, player, dir):
        super().__init__(player, dir)

    def execute(self, isMoving):
        self.actor.verticalMovement(self.direction, isMoving)

class InputHandler:
    def __init__(self, player, publisher):
        self.publisher = publisher

        self.W_command = VerticalMovement(player, -1)
        self.S_command = VerticalMovement(player, 1)
        self.A_command = HorizontalMovement(player, -1)
        self.D_command = HorizontalMovement(player, 1)

    def handleInput(self, event, controls):
        if event.type == pygame.KEYDOWN:
            if(config.currentLevel == config.LevelEnum.Platformer.value):
                if event.key == pygame.key.key_code(controls['jump']):
                    self.W_command.execute(True)

                if event.key == pygame.key.key_code(controls['sit_down']):
                    self.S_command.execute(True)

                if event.key == pygame.key.key_code(controls['left']):
                    self.A_command.execute(True)

                if event.key == pygame.key.key_code(controls['right']):
                    self.D_command.execute(True)

            if(config.currentLevel == config.LevelEnum.Strategy.value):
                if event.key == pygame.key.key_code(controls['front']):
                    self.W_command.execute(True)

                if event.key == pygame.key.key_code(controls['back']):
                    self.S_command.execute(True)

                if event.key == pygame.key.key_code(controls['left']):
                    self.A_command.execute(True)

                if event.key == pygame.key.key_code(controls['right']):
                    self.D_command.execute(True)

            if event.key == pygame.K_ESCAPE:
                config.currentLevel = config.UIEnum.Pause.value

        if event.type == pygame.KEYUP:
            if(config.currentLevel == config.LevelEnum.Platformer.value):
                if event.key == pygame.key.key_code(controls['jump']):
                    self.W_command.execute(False)

                if event.key == pygame.key.key_code(controls['sit_down']):
                    self.S_command.execute(False)

                if event.key == pygame.key.key_code(controls['left']):
                    self.A_command.execute(False)

                if event.key == pygame.key.key_code(controls['right']):
                    self.D_command.execute(False)

            if(config.currentLevel == config.LevelEnum.Strategy.value):
                if event.key == pygame.key.key_code(controls['front']):
                    self.W_command.execute(False)

                if event.key == pygame.key.key_code(controls['back']):
                    self.S_command.execute(False)

                if event.key == pygame.key.key_code(controls['left']):
                    self.A_command.execute(False)

                if event.key == pygame.key.key_code(controls['right']):
                    self.D_command.execute(False)
 