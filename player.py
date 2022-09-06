import pygame
from pygame.math import Vector2
from config import *
from untils import normalize


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, image):
        super().__init__(group)

        # 基本属性
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        # 物理属性
        self.direction = Vector2((0, -1))
        self.pos = Vector2(self.rect.center)
        self.speed = PLAYER_MAXSPEED

    # 用户按键操作
    def input(self):
        keys = pygame.key.get_pressed()
        directionVector = Vector2()
        if keys[pygame.K_LEFT]:
            directionVector.x -= 1
        if keys[pygame.K_RIGHT]:
            directionVector.x += 1
        if keys[pygame.K_UP]:
            directionVector.y -= 1
        if keys[pygame.K_DOWN]:
            directionVector.y += 1
        self.direction = normalize(directionVector)

    # 玩家移动
    def move(self, speed):
        self.rect.center += self.direction * speed

    def update(self, dt):
        self.input()
        self.move(self.speed)