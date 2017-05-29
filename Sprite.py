import pygame as pg
from Setting import *
vector = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collision_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vector(0, 0)
        self.pos = vector(x, y) * TILESIZE
        self.rotate = 0

    def get_keys(self):
        self.rotate_speed = 0
        self.vel = vector(0, 0)
        # looks for the pressed key
        keys = pg.key.get_pressed()
        # player's control commands
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotate_speed = PLAYER_ROTATIONAL_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotate_speed = -PLAYER_ROTATIONAL_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vector(PLAYER_SPEED, 0).rotate(-self.rotate)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vector(-PLAYER_SPEED / 2, 0).rotate(-self.rotate)

    def update(self):
        self.get_keys()
        self.rotate = (self.rotate + self.rotate_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        # allows player to slide horizontally
        self.hit_rect.centerx = self.pos.x
        collision_with_walls(self, self.game.walls, 'x')
        # allows player to slide vertically
        self.hit_rect.centery = self.pos.y
        collision_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vector(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rotate = 0
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

    def update(self):
        self.rotate = (self.game.player.pos - self.pos).angle_to(vector(1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vector(MOB_SPEED, 0).rotate(-self.rotate)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + self.acc * self.game.dt ** 2
        # allows player to slide horizontally
        self.hit_rect.centerx = self.pos.x
        collision_with_walls(self, self.game.walls, 'x')
        # allows player to slide vertically
        self.hit_rect.centery = self.pos.y
        collision_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center