import enum, logging

class UIEnum(enum.Enum):
    Main_menu = 0
    Inform = 1
    Settings = 2
    Pause = 3
    Game = 4

class EventsEnum(enum.Enum):
    movement = 0
    jump = 1
    achievement = 2

class ListLevel(enum.Enum):
    Strategy = 0
    Shooter = 1
    Platformer = 2

state = UIEnum.Main_menu.value
prev_state = state

logging.basicConfig(level= logging.DEBUG, filename= "logs/logs.log", filemode= "w")

TILE_SIZE = 64
WIDTH, HEIGHT = 1280, 720
FPS = 60                        # limits FPS to 60
SPEED_SCALE = 30
FONT_SIZE = 16
OFFSET = 10

savedValues = {}

LEVEL_MAP = [
'                            ',
'                            ',
'                            ',
'                            ',
'   P                        ',
'                            ',
'                            ',
'                            ',
'      C      C          C   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXX']

CAMERA_BORDERS = {
	'left': 100,
	'right': 200,
	'top':100,
	'bottom': 150
}

curr_window_width = WIDTH
curr_window_height = HEIGHT
