import pygame as pg 

# Colors (Red, Green Blue)
WHITE = (255, 255,255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN  = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
TAN = (210, 180, 140)

# Game Properties
WIDTH = 768     # 24 * 32
HEIGHT = 640     # 20 * 32
FPS = 60
TITLE = "TileGame"
BGCOLOR = TAN

# Map Settings
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
WALL_IMG = 'tile_03.png'

# Player Settings
PLAYER_SPEED = 300
PLAYER_ROTATIONAL_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# Mob Settings
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)