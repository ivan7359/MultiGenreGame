import pygame, pygame_gui
import logging

from observer import *
from command import *

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

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        logging.basicConfig(level=logging.DEBUG, filename="logs/logs.log",filemode="w")
        logging.info("Game was started")
        self.clock = pygame.time.Clock()
        self.gameState = GameState(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.publisher = Subject()
        self.publisher.addObserver(Audio())
        self.inputHandler = InputHandler(self.screen)

        self.running = True
        self.speed = 7
        self.dt = 0                 # delta time in seconds since last frame

        self.moveCommandX = 0
        self.moveCommandY = 0 


############################## UI Events ###############################
        self.CurrPercent = 70
        self.img = pygame.image.load('media/pygame_logo_100x100.png')

        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 4.41, HEIGHT / 2.93), (200, 70)), text='Play', manager=self.manager)
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 4.41, HEIGHT / 1.93), (200, 70)), text='Settings', manager=self.manager)
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 4.41, HEIGHT / 1.43), (200, 70)), text='Exit', manager=self.manager)
        self.info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 42.67, HEIGHT / 24), (69, 69)), text='Info', manager=self.manager)
        self.left_arrow_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 1.64, HEIGHT / 1.43), (94, 50)), text='Left arrow', manager=self.manager)
        self.right_arrow_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 1.38, HEIGHT / 1.43), (94, 50)), text='Right arrow', manager=self.manager)
        self.label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH / 3.9, HEIGHT / 7.2), (623, 70)), text="MultiGenreGame", manager=self.manager)
        self.image = pygame_gui.elements.UIImage(pygame.Rect((WIDTH / 1.86, HEIGHT / 2.93), (427, 240)), self.img, self.manager)
        
        # self.slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((15, 75), (300, 25)), start_value=0, value_range=[0, 100], manager=self.manager)
        # self.text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((15, 115), (300, 300)), manager=self.manager)
        # self.menu = pygame_gui.elements.UIDropDownMenu(options_list=["1", "2", "3"], starting_option="1", relative_rect=pygame.Rect((15, 415), (100, 100)), manager=self.manager)
        # self.selectionList = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((15, 530), (100, 100)), item_list=["1", "2", "3"], manager=self.manager)
        # self.textEntryLine = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((15, 645), (300, 25)), manager=self.manager)
        # self.statusBar = pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect((15, 685), (300, 25)), manager=self.manager, percent_method=self.getCurrPercent)
########################################################################

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def getCurrPercent(self):
        return self.CurrPercent

    def processInput(self):
        self.moveCommandX = 0
        self.moveCommandY = 0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            
        command = self.inputHandler.handleInput()
        if(command):
            command.execute()

        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_w]:
        #     self.moveCommandY -= self.speed * self.dt
        #     self.publisher.notify(AudioEnum.jump.name)
        # if keys[pygame.K_s]:
        #     self.moveCommandY += self.speed * self.dt
        #     self.publisher.notify(AudioEnum.run.name)
        # if keys[pygame.K_a]:
        #     self.moveCommandX -= self.speed * self.dt
        #     self.publisher.notify(AudioEnum.run.name)
        # if keys[pygame.K_d]:
        #     self.moveCommandX += self.speed * self.dt
        #     self.publisher.notify(AudioEnum.run.name)

############################## UI Events ###############################
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == self.play_button:
                    print('Button play was pressed!')
              if event.ui_element == self.settings_button:
                    print('Button settings was pressed!')
              if event.ui_element == self.exit_button:
                    print('Button exit was pressed!')
              if event.ui_element == self.info_button:
                    print('Button info was pressed!')
              if event.ui_element == self.left_arrow_button:
                    print('Button left arrow was pressed!')
              if event.ui_element == self.right_arrow_button:
                    print('Button right arrow was pressed!')
            
            # if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            #   if event.ui_element == self.slider:
            #         print('current slider value:', event.value)

            # if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            #     if event.ui_element == self.text:
            #         print("Changed text:", event.text)

            #     if event.ui_element == self.textEntryLine:
            #         print("Changed textEntryLine:", event.text)

            # if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            #     print("Selected option:", event.text)

            # if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            #     if event.ui_element == self.selectionList:
            #         print("Selected item:", event.text)

            self.manager.process_events(event)
########################################################################

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.moveCommandY -= self.speed * self.dt
        if keys[pygame.K_s]:
            self.moveCommandY += self.speed * self.dt
        if keys[pygame.K_a]:
            self.moveCommandX -= self.speed * self.dt
        if keys[pygame.K_d]:
            self.moveCommandX += self.speed * self.dt
        
        if keys[pygame.K_LEFT]:
            self.CurrPercent -= 1

    def update(self):
        # We delegate store and update game data to GameState class
        self.gameState.update(self.moveCommandX, self.moveCommandY)
        self.manager.update(self.dt)

    def render(self):
        self.screen.fill("black")
        pygame.draw.circle(self.screen, "red", (self.gameState.x, self.gameState.y), 30)
        
        self.manager.draw_ui(self.screen)
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