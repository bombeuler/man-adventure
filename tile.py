import pygame
from config import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups,image,spriteType='staticbody'):
        super().__init__(groups)
        self.spriteType = spriteType
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-6 * SCALE_RATE)

    
    def __getattr__(self, _):
            return None
