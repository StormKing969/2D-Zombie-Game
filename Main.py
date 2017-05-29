import pygame as pg
import sys
from os import path
from Setting import *
from Sprite import *
from LevelMaps import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.join(path.dirname(__file__), 'Levels')
        img_folder = path.join(path.dirname(__file__), 'Images')
        # Map
        self.map = Map(path.join(game_folder, 'Map.txt'))
        # Borders
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        # Player
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        # Mob
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        # gives each value in the row an index number
        for row, tiles in enumerate(self.map.data):
        	# gives each value in the column an index number
        	for col, tile in enumerate(tiles):
        		if tile == '1':
        			# return the coordinates onto which a wall is drawn 
        			Wall(self, col, row)
        		if tile == 'M':
        			# return the coordinates onto which a wall is drawn 
        			Mob(self, col, row)
        		if tile == 'P':
        			# returns the spwaning location of the player
        			self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
        	# draws the horizontal lines on the screen
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
        	# draws the vertical lines on the screen 
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.draw_grid()
        for sprite in self.all_sprites:
        	self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()