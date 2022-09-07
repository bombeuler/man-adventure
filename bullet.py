import pygame
from pygame.math import Vector2
from config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, pos, speed,damage, direction,origin):
        super().__init__(groups)
        self.spriteType = 'bullet'
        self.fly =True
        bulletImage = pygame.image.load(
            f'{ASSETS_PATH}/real_bullet.png').convert_alpha()
        self.image = pygame.transform.scale(bulletImage,
                                            (SCALE_RATE * 4, SCALE_RATE * 4))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.once = True
        self.damage = damage
        self.distance = 0
        self.direction = direction
        self.origin = origin

    def __getattr__(self, _):
            return None


    def move(self):
        xDt = self.direction.x * self.speed
        yDt = self.direction.y * self.speed
        self.rect.x += xDt
        self.rect.y += yDt
        self.distance += Vector2((xDt,yDt)).magnitude()

    def update(self,dt):
        super().update(dt)
        self.move()
        if self.distance >=BULLET_MAXDISTANCE:
            self.kill()