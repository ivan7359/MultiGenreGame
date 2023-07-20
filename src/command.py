import pygame

class Command:
    def execute(self, actor = None):
        pass

class Run(Command):
    def __init__(self, dir):
        self.direction = dir

    def execute(self, actor = None):
        actor.move(self.direction)
        print("run")

class Jump(Command):
    def execute(self, actor = None):
        actor.jump()
        print("jump")

class InputHandler:
    def __init__(self, screen):
        self.W_command = Jump()
        self.S_command = Command()
        self.A_command = Run(-1)
        self.D_command = Run(1)

        self.keys = None
        self.screen = screen

    def handleInput(self, event = None):
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         return self.W_command
        #     if event.key == pygame.K_s:
        #         return self.S_command
        #     if event.key == pygame.K_a:
        #         return self.A_command
        #     if event.key == pygame.K_d:
        #         return self.D_command

        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_w]:
            return self.W_command
        if self.keys[pygame.K_s]:
            # return self.S_command
            self.changeKeys(self.keys[pygame.K_w], self.keys[pygame.K_a])
        if self.keys[pygame.K_a]:
            return self.A_command
        if self.keys[pygame.K_d]:
            return self.D_command
        
        # if self.keys[pygame.K_1]:
        #     info = pygame.display.Info() 
        #     pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)

    def changeKeys(self, prev, curr):
        pass