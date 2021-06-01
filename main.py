import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        sprites_folder = path.join(game_folder, 'sprites')
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.player_spr = pg.image.load(
            path.join(sprites_folder, PLAYER_SPR)).convert_alpha()  # Player Sprite
        self.bullet_spr = pg.image.load(
            path.join(sprites_folder, BULLET_SPR)).convert_alpha()  # Bullet Sprite
        self.zombie_spr = pg.image.load(
            path.join(sprites_folder, ZOMBIE_IMAGE)).convert_alpha()  # Zombie Sprite
        self.wall_spr = pg.image.load(
            path.join(sprites_folder, WALL_IMAGE)).convert_alpha()  # Wall Sprite
        self.wall_spr = pg.transform.scale(self.wall_spr, (TILESIZE, TILESIZE))

    def sprite(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        # Explain how enumerate works next class
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'Z':
                    Zombie(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)  # Camera Object

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

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # player controls
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
    g.sprite()
    g.run()
    g.show_go_screen()
