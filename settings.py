import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (148, 127, 105)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Top Down Shooter"
BGCOLOR = BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player Settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250.0
PLAYER_SPR = 'player.gif'
PLAYER_HIT_RECT = pg.Rect(0, 0, 48, 48)  # Hitbox


# Wall settings
WALL_IMAGE = "SLIMBRICKS.png"
FLOOR_IMAGE = "FLOOR.png"

# Zombie Settings
ZOMBIE_IMAGE = "ZOMBIE.png"
ZOMBIE_SPEED = 200
ZOMBIE_WALK_SPEED = 100
ZOMBIE_HIT_RECT = pg.Rect(0, 0, 40, 40)

# Weapon Settings
BULLET_SPR = 'bullet.png'
BULLET_SPEED = 550
BULLET_LIFETIME = 1200
BULLET_RATE = 150
BARREL_OFFSET = vec(20, 10)  # Spawn position of the bullet
RECOIL = 200
BULLET_SPREAD = 10
