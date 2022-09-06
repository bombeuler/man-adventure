import pygame
from config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self,groups,pos,speed,direction):
        super().__init__(groups)
        bulletImage = pygame.image.load(
            f'{ASSETS_PATH}/real_bullet.png').convert_alpha()
        self.image = pygame.transform.scale(bulletImage,(SCALE_RATE *4,SCALE_RATE *4))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.direction = direction

    def update(self,dt):
        super().update(dt)