import pygame
from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.rect = self.image.get_rect(topleft = pos)