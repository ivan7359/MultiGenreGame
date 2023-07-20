import logging

logging.basicConfig(level= logging.DEBUG, filename= "logs/logs.log", filemode= "w")

TILE_SIZE = 64

WIDTH, HEIGHT = 1280, 720
FPS = 60                        # limits FPS to 60
SPEED_SCALE = 30

FONT_SIZE = 16

LEVEL_MAP = [
'                            ',
'                            ',
'                            ',
'                            ',
'   P                        ',
'                            ',
'                            ',
'                            ',
'                            ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXX']

CAMERA_BORDERS = {
	'left': 100,
	'right': 200,
	'top':100,
	'bottom': 150
}
