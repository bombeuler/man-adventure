import pygame
from pygame.math import Vector2
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface(SCREEN_SIZE)
        self.rect = self.image.get_rect(center=pos)

        self.direction = Vector2((0, -1))
        self.pos = Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            print('up')

    def update(self, dt):
        self.input()