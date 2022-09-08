import pygame
from config import *

class Item(pygame.sprite.Sprite):
    def __init__(self,pos,groups,image,effect):
        super().__init__(groups)
        self.image = image
        self.spriteType = "item"
        self.rect = self.image.get_rect(topleft=pos)
        self.effect = effect

    def __getattr__(self, _):
        return None

