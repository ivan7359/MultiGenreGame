import pygame, pygame_gui
import logging

from observer import *
from command import *
import config

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
        
        OFFSET = 10
        label_game_width = 623
        button_width = 200
        button_height = 70
        image_width = 427
        arrow_btn_width = 94
        arrow_btn_height = 50
        label_sp_width = 160
        label_sp_height = 55
        btn_Back_ok_width = 100
        btn_Back_ok_height = 50
        label_asc_width = 85
        label_asc_height = 35
        label_settings_width = 200 # где-то получилось, что текст сдвинулся, т.к. расположение текста в центре, а нужно сделать по левому краю
        label_settings_height = 25
        slider_width = 163
        slider_height = 20
        menu_width = 123
        menu_height = 20
        textEntryLine_width = 80
        textEntryLine_height = 28

    
# Main menu
        self.info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((OFFSET * 3, OFFSET * 3), (70, 70)), text='Info', manager=self.manager)
        self.label_name_game = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(( (WIDTH / 2) - (label_game_width / 2), HEIGHT / 8), (label_game_width, 70)), text="MultiGenreGame", manager=self.manager)
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 3) - (button_width / 2) - (OFFSET * 4), (HEIGHT / 3)), (button_width, button_height)), text='Play', manager=self.manager)
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 3) - (button_width / 2) - (OFFSET * 4), (HEIGHT / 3) + (button_height + (OFFSET * 5))), (button_width, button_height)), text='Settings', manager=self.manager)
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 3) - (button_width / 2) - (OFFSET * 4), (HEIGHT / 3) + ((button_height  + (OFFSET * 5)) * 2)), (button_width, button_height)), text='Exit', manager=self.manager)
        self.left_arrow_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH * 0.66) - (arrow_btn_width) - OFFSET, (HEIGHT * 0.66) + (OFFSET * 2)), (arrow_btn_width, arrow_btn_height)), text='Left arrow', manager=self.manager)
        self.right_arrow_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH * 0.66) + OFFSET, (HEIGHT * 0.66) + (OFFSET * 2)), (arrow_btn_width, arrow_btn_height)), text='Right arrow', manager=self.manager)
        self.image = pygame_gui.elements.UIImage(pygame.Rect(((WIDTH * 0.66) - (image_width / 2), (HEIGHT / 3)), (image_width, 240)), self.img, self.manager)
# Settings        
        self.info_settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((OFFSET * 3, OFFSET * 3), (70, 70)), text='Info', manager=self.manager)
        self.label_name_game_settings = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(( (WIDTH / 2) - (label_game_width / 2), HEIGHT / 8), (label_game_width, 70)), text="MultiGenreGame", manager=self.manager)
        self.label_settings = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 2) - (label_sp_width / 2), (HEIGHT / 3) - (label_sp_height / 2) - OFFSET), (label_sp_width, label_sp_height)), text="Settings", manager=self.manager)
        self.Back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((OFFSET * 3, (HEIGHT - btn_Back_ok_height) - (OFFSET * 3)), (btn_Back_ok_width, btn_Back_ok_height)), text='Back', manager=self.manager)
        self.OK_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH - btn_Back_ok_width) - (OFFSET * 3), (HEIGHT - btn_Back_ok_height) - (OFFSET * 3)), (btn_Back_ok_width, btn_Back_ok_height)), text='OK', manager=self.manager)
        self.label_settings_audio = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_asc_width - (OFFSET * 14) , (HEIGHT / 3) + (OFFSET * 2.2)), (label_asc_width, label_asc_height)), text="Audio", manager=self.manager)
        self.label_settings_sound = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT / 3) + (OFFSET * 6.9)), (label_settings_width, label_settings_height)), text="Sound", manager=self.manager)
        self.slider_sound = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 0.5), (HEIGHT / 3) + (OFFSET * 6.9)), (slider_width, slider_height)), start_value=0, value_range=[0, 100], manager=self.manager)
        self.label_settings_music = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT / 2) + (OFFSET * 0.8)), (label_settings_width, label_settings_height)), text="Music", manager=self.manager)
        self.slider_music = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 0.5), (HEIGHT / 2) + (OFFSET * 0.8)), (slider_width, slider_height)), start_value=0, value_range=[0, 100], manager=self.manager)
        self.label_settings_screen = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_asc_width - (OFFSET * 14) , (HEIGHT * 0.66) - (label_asc_height / 2) - (OFFSET * 1.7)), (label_asc_width, label_asc_height)), text="Screen", manager=self.manager)
        self.label_settings_resolution = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 1.3)), (label_settings_width, label_settings_height)), text="Resolution", manager=self.manager)
        self.menu_resolution = pygame_gui.elements.UIDropDownMenu(options_list=["1280 x 720", "2", "3"], starting_option="1280 x 720", relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 1.3)), (menu_width, menu_height)), manager=self.manager)
        self.label_settings_display_mode = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 6.2)), (label_settings_width, label_settings_height)), text="Display mode", manager=self.manager)
        self.menu_display_mode = pygame_gui.elements.UIDropDownMenu(options_list=["Fullsreen", "2", "3"], starting_option="Fullscreen", relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 6.2)), (menu_width, menu_height)), manager=self.manager)
        self.label_settings_brightness = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 11.3)), (label_settings_width, label_settings_height)), text="Brightness", manager=self.manager)
        self.slider_brightness = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 11.3)), (slider_width, slider_height)), start_value=0, value_range=[0, 100], manager=self.manager)
        self.label_settings_controls = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH / 1.93, HEIGHT / 2.75), (label_asc_width, label_asc_height)), text="Controls", manager=self.manager)
        self.label_controls_left = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 5)), (label_settings_width, label_settings_height)), text="Left", manager=self.manager)
        self.textEntryLine_left = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 4.8))), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_right = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 6) + label_settings_height), (label_settings_width, label_settings_height)), text="Right", manager=self.manager)
        self.textEntryLine_right = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 5.6) + textEntryLine_height)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_jump_pl= pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 7) + (label_settings_height * 2)), (label_settings_width, label_settings_height)), text="Jump (platformer)", manager=self.manager)
        self.textEntryLine_jump_pl = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 6.4) + textEntryLine_height * 2)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_jump_sh = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 8) + (label_settings_height * 3)), (label_settings_width, label_settings_height)), text="Jump (shooter)", manager=self.manager)
        self.textEntryLine_jump_sh = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 7.2) + textEntryLine_height * 3)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_duck_down_pl = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 9) + (label_settings_height * 4)), (label_settings_width, label_settings_height)), text="Duck down (platformer)", manager=self.manager)
        self.textEntryLine_duck_down_pl = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 8) + textEntryLine_height * 4)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_duck_down_sh = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 10) + (label_settings_height * 5)), (label_settings_width, label_settings_height)), text="Duck down (shooter)", manager=self.manager)
        self.textEntryLine_duck_down_sh = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 8.8) + textEntryLine_height * 5)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_melee_pl = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 11) + (label_settings_height * 6)), (label_settings_width, label_settings_height)), text="Melee (platformer)", manager=self.manager)
        self.textEntryLine_melee_pl = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 9.6) + textEntryLine_height * 6)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_melee_sh = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 12) + (label_settings_height * 7)), (label_settings_width, label_settings_height)), text="Melee (platformer)", manager=self.manager)
        self.textEntryLine_melee_sh = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 10.4) + textEntryLine_height * 7)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_fire_pl = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 13) + (label_settings_height * 8)), (label_settings_width, label_settings_height)), text="Fire (shooter)", manager=self.manager)
        self.textEntryLine_fire_pl = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 11.2) + textEntryLine_height * 8)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.label_controls_Weapon_change_sh = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 14) + (label_settings_height * 9)), (label_settings_width, label_settings_height)), text="Weapon change (shooter)", manager=self.manager)
        self.textEntryLine_Weapon_change_sh = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 12) + textEntryLine_height * 9)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)



# Pause
        self.label_name_game_pause = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(( (WIDTH / 2) - (label_game_width / 2), HEIGHT / 8), (label_game_width, 70)), text="MultiGenreGame", manager=self.manager)
        self.label_pause = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 2) - (label_sp_width / 2), (HEIGHT / 3) - (label_sp_height / 2)), (label_sp_width, label_sp_height)), text="Pause", manager=self.manager)
        self.continue_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 2) - (button_width / 2), (HEIGHT / 3) + (OFFSET * 5)), (button_width, button_height)), text='Continue', manager=self.manager)
        self.settings_pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 2) - (button_width / 2), (HEIGHT / 3) + (OFFSET * 8.5) + button_height), (button_width, button_height)), text='Settings', manager=self.manager)
        self.exit_pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 2) - (button_width / 2), (HEIGHT / 3) + (OFFSET * 12) + (button_height * 2)), (button_width, button_height)), text='Exit', manager=self.manager)
              
        # self.text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((15, 115), (300, 300)), manager=self.manager)
        #self.selectionList = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((15, 530), (100, 100)), item_list=["1", "2", "3"], manager=self.manager)
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
# Maim_menu             
              if event.ui_element == self.play_button:
                    print('Button play was pressed!')
                    config.state = config.UIEnum.Game.value
              if event.ui_element == self.settings_button:
                    config.state = config.UIEnum.Settings.value
                    print('Button settings was pressed!')
              if event.ui_element == self.exit_button:
                    print('Button exit was pressed!')
              if event.ui_element == self.info_button:
                    print('Button info was pressed!')
              if event.ui_element == self.left_arrow_button:
                    print('Button left arrow was pressed!')
              if event.ui_element == self.right_arrow_button:
                    print('Button right arrow was pressed!')
# Settings
              if event.ui_element == self.info_settings_button:
                    print('Button info was pressed!')
              if event.ui_element == self.Back_button:
                    config.state = config.UIEnum.Main_menu.value
                    print('Button Back was pressed!')
              if event.ui_element == self.OK_button:
                    config.state = config.UIEnum.Main_menu.value
                    print('Button OK was pressed, changes saved!')
# Pause
              if event.ui_element == self.continue_button:
                    config.state = config.UIEnum.Game.value
                    print('Button continue was pressed!')
              if event.ui_element == self.settings_pause_button:
                    config.state = config.UIEnum.Settings.value
                    print('Button settings was pressed!')  
              if event.ui_element == self.exit_pause_button:
                    config.state = config.UIEnum.Main_menu.value
                    print('Button exit was pressed!')
            
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
        command = self.inputHandler.handleInput()
        if(command):
            command.execute()

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
        if (config.state == config.UIEnum.Main_menu.value):
            self.play_button.show()
            self.settings_button.show()
            self.exit_button.show()
            self.info_button.show()
            self.left_arrow_button.show()
            self.right_arrow_button.show()
            self.label_name_game.show()
            self.image.show()

            self.label_name_game_pause.hide()
            self.label_pause.hide()
            self.continue_button.hide()
            self.settings_pause_button.hide()
            self.exit_pause_button.hide()

            self.info_settings_button.hide()
            self.label_name_game_settings.hide()
            self.label_settings.hide()
            self.Back_button.hide()
            self.OK_button.hide()
            self.label_settings_audio.hide()
            self.label_settings_sound.hide()
            self.slider_sound.hide()
            self.label_settings_music.hide()
            self.slider_music.hide()
            self.label_settings_screen.hide()
            self.label_settings_resolution.hide()
            self.menu_resolution.hide()
            self.label_settings_display_mode.hide()
            self.menu_display_mode.hide()
            self.label_settings_brightness.hide()
            self.slider_brightness.hide()
            self.label_settings_controls.hide()
            self.label_controls_left.hide()
            self.textEntryLine_left.hide() 
            self.label_controls_right.hide()
            self.textEntryLine_right.hide()
            self.label_controls_jump_pl.hide()
            self.textEntryLine_jump_pl.hide()
            self.label_controls_jump_sh.hide() 
            self.textEntryLine_jump_sh.hide()
            self.label_controls_duck_down_pl.hide() 
            self.textEntryLine_duck_down_pl.hide() 
            self.label_controls_duck_down_sh.hide()
            self.textEntryLine_duck_down_sh.hide() 
            self.label_controls_melee_pl.hide() 
            self.textEntryLine_melee_pl.hide() 
            self.label_controls_melee_sh.hide() 
            self.textEntryLine_melee_sh.hide() 
            self.label_controls_fire_pl.hide()  
            self.textEntryLine_fire_pl.hide() 
            self.label_controls_Weapon_change_sh.hide()
            self.textEntryLine_Weapon_change_sh.hide()
        if (config.state == config.UIEnum.Game.value):
            self.play_button.hide()
            self.settings_button.hide()
            self.exit_button.hide()
            self.info_button.hide()
            self.left_arrow_button.hide()
            self.right_arrow_button.hide()
            self.label_name_game.hide()
            self.image.hide()

            self.label_name_game_pause.hide()
            self.label_pause.hide()
            self.continue_button.hide()
            self.settings_pause_button.hide()
            self.exit_pause_button.hide()


            self.info_settings_button.hide()
            self.label_name_game_settings.hide()
            self.label_settings.hide()
            self.Back_button.hide()
            self.OK_button.hide()
            self.label_settings_audio.hide()
            self.label_settings_sound.hide()
            self.slider_sound.hide()
            self.label_settings_music.hide()
            self.slider_music.hide()
            self.label_settings_screen.hide()
            self.label_settings_resolution.hide()
            self.menu_resolution.hide()
            self.label_settings_display_mode.hide()
            self.menu_display_mode.hide()
            self.label_settings_brightness.hide()
            self.slider_brightness.hide()
            self.label_settings_controls.hide()
            self.label_controls_left.hide()
            self.textEntryLine_left.hide() 
            self.label_controls_right.hide()
            self.textEntryLine_right.hide()
            self.label_controls_jump_pl.hide()
            self.textEntryLine_jump_pl.hide()
            self.label_controls_jump_sh.hide() 
            self.textEntryLine_jump_sh.hide()
            self.label_controls_duck_down_pl.hide() 
            self.textEntryLine_duck_down_pl.hide() 
            self.label_controls_duck_down_sh.hide()
            self.textEntryLine_duck_down_sh.hide() 
            self.label_controls_melee_pl.hide() 
            self.textEntryLine_melee_pl.hide() 
            self.label_controls_melee_sh.hide() 
            self.textEntryLine_melee_sh.hide() 
            self.label_controls_fire_pl.hide()  
            self.textEntryLine_fire_pl.hide() 
            self.label_controls_Weapon_change_sh.hide()
            self.textEntryLine_Weapon_change_sh.hide()
        if (config.state == config.UIEnum.Pause.value):
            self.play_button.hide()
            self.settings_button.hide()
            self.exit_button.hide()
            self.info_button.hide()
            self.left_arrow_button.hide()
            self.right_arrow_button.hide()
            self.label_name_game.hide()
            self.image.hide()

            self.label_name_game_pause.show()
            self.label_pause.show()
            self.continue_button.show()
            self.settings_pause_button.show()
            self.exit_pause_button.show()

            self.info_settings_button.hide()
            self.label_name_game_settings.hide()
            self.label_settings.hide()
            self.Back_button.hide()
            self.OK_button.hide()
            self.label_settings_audio.hide()
            self.label_settings_sound.hide()
            self.slider_sound.hide()
            self.label_settings_music.hide()
            self.slider_music.hide()
            self.label_settings_screen.hide()
            self.label_settings_resolution.hide()
            self.menu_resolution.hide()
            self.label_settings_display_mode.hide()
            self.menu_display_mode.hide()
            self.label_settings_brightness.hide()
            self.slider_brightness.hide()
            self.label_settings_controls.hide()
            self.label_controls_left.hide()
            self.textEntryLine_left.hide() 
            self.label_controls_right.hide()
            self.textEntryLine_right.hide()
            self.label_controls_jump_pl.hide()
            self.textEntryLine_jump_pl.hide()
            self.label_controls_jump_sh.hide() 
            self.textEntryLine_jump_sh.hide()
            self.label_controls_duck_down_pl.hide() 
            self.textEntryLine_duck_down_pl.hide() 
            self.label_controls_duck_down_sh.hide()
            self.textEntryLine_duck_down_sh.hide() 
            self.label_controls_melee_pl.hide() 
            self.textEntryLine_melee_pl.hide() 
            self.label_controls_melee_sh.hide() 
            self.textEntryLine_melee_sh.hide() 
            self.label_controls_fire_pl.hide()  
            self.textEntryLine_fire_pl.hide() 
            self.label_controls_Weapon_change_sh.hide()
            self.textEntryLine_Weapon_change_sh.hide()
        if (config.state == config.UIEnum.Settings.value):
            self.play_button.hide()
            self.settings_button.hide()
            self.exit_button.hide()
            self.info_button.hide()
            self.left_arrow_button.hide()
            self.right_arrow_button.hide()
            self.label_name_game.hide()
            self.image.hide()

            self.label_name_game_pause.hide()
            self.label_pause.hide()
            self.continue_button.hide()
            self.settings_pause_button.hide()
            self.exit_pause_button.hide()

            self.info_settings_button.show()
            self.label_name_game_settings.show()
            self.label_settings.show()
            self.Back_button.show()
            self.OK_button.show()
            self.label_settings_audio.show()
            self.label_settings_sound.show()
            self.slider_sound.show()
            self.label_settings_music.show()
            self.slider_music.show()
            self.label_settings_screen.show()
            self.label_settings_resolution.show()
            self.menu_resolution.show()
            self.label_settings_display_mode.show()
            self.menu_display_mode.show()
            self.label_settings_brightness.show()
            self.slider_brightness.show()
            self.label_settings_controls.show()
            self.label_controls_left.show()
            self.textEntryLine_left.show()
            self.label_controls_right.show()
            self.textEntryLine_right.show()
            self.label_controls_jump_pl.show()
            self.textEntryLine_jump_pl.show()
            self.label_controls_jump_sh.show() 
            self.textEntryLine_jump_sh.show()
            self.label_controls_duck_down_pl.show() 
            self.textEntryLine_duck_down_pl.show()
            self.label_controls_duck_down_sh.show()
            self.textEntryLine_duck_down_sh.show()
            self.label_controls_melee_pl.show()
            self.textEntryLine_melee_pl.show()
            self.label_controls_melee_sh.show() 
            self.textEntryLine_melee_sh.show() 
            self.label_controls_fire_pl.show() 
            self.textEntryLine_fire_pl.show()
            self.label_controls_Weapon_change_sh.show()
            self.textEntryLine_Weapon_change_sh.show()
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