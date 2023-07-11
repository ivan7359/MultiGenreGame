import pygame, pygame_gui
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
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        logging.basicConfig(level=logging.DEBUG, filename="logs/logs.log",filemode="w")
        logging.info("Game was started")
        self.clock = pygame.time.Clock()
        self.gameState = GameState(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2))

        self.running = True
        self.speed = 7
        self.dt = 0                 # delta time in seconds since last frame

        self.moveCommandX = 0
        self.moveCommandY = 0 


############################## UI Events ###############################
        self.CurrPercent = 70
        self.img = pygame.image.load('media/pygame_logo_100x100.png')

        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (100, 50)), text='Say Hello', manager=self.manager)
        self.slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((15, 75), (300, 25)), start_value=0, value_range=[0, 100], manager=self.manager)
        self.text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((15, 115), (300, 300)), manager=self.manager)
        self.menu = pygame_gui.elements.UIDropDownMenu(options_list=["1", "2", "3"], starting_option="1", relative_rect=pygame.Rect((15, 415), (100, 100)), manager=self.manager)
        self.selectionList = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((15, 530), (100, 100)), item_list=["1", "2", "3"], manager=self.manager)
        self.textEntryLine = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((15, 645), (300, 25)), manager=self.manager)
        self.statusBar = pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect((15, 685), (300, 25)), manager=self.manager, percent_method=self.getCurrPercent)
        self.label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((330, 15), (100, 25)), text="just a label", manager=self.manager)
        self.image = pygame_gui.elements.UIImage(pygame.Rect((330, 50), (100, 100)), self.img, self.manager)
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

############################## UI Events ###############################
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == self.hello_button:
                    print('Button was pressed!')
            
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
              if event.ui_element == self.slider:
                    print('current slider value:', event.value)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.text:
                    print("Changed text:", event.text)

                if event.ui_element == self.textEntryLine:
                    print("Changed textEntryLine:", event.text)

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                print("Selected option:", event.text)

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.selectionList:
                    print("Selected item:", event.text)

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