import pygame as pg
from random import uniform
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    # Collision with X axis
    if dir == 'x':
        hits = pg.sprite.spritecollide(
            sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    # Collision with Y axis
    if dir == 'y':
        hits = pg.sprite.spritecollide(
            sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + \
                    sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_spr
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0

    def move(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                # Create a new bullet if player presses space and previous bullet been out for long enough
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                # Spawn bullet at the start of the barrel, instead of the center of the player
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                # Apply recoil to the player after shooting
                self.vel = vec(-RECOIL, 0).rotate(-self.rot)

    def update(self):
        self.move()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_spr, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Zombie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.zombies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_spr
        self.rect = self.image.get_rect()
        self.hit_rect = ZOMBIE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)  # Zombie Velocity
        # Zombie Accelaration, don't let zombie make sharp turns too quickly
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        # Turn in player's direction
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(
            self.game.zombie_spr, self.rot)  # Update the image rotation
        self.rect = self.image.get_rect()  # Collision hitbox
        self.rect.center = self.pos
        self.acc = vec(ZOMBIE_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1  # Slow down the enemy as he starts moving
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt * 2
        # Enemy collision with x walls
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        # Enemy collision with y walls
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        # Allign enemies model with enemies hitbox
        self.rect.center = self.hit_rect.center


class Bullet (pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_spr
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        # Bullet spread while shooting
        spread = uniform(-BULLET_SPREAD, BULLET_SPREAD)
        # Move the bullet in the direction of the spread
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.rot = 0

    def update(self):
        #self.rot = (self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(
            self.game.bullet_spr, self.rot)  # Update bullet rotation
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos.rotate(-self.rot)
        # Destroy bullet if it collides with the wall
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:  # Destroy bullet if it's been out for too long
            self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_spr
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
