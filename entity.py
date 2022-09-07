import pygame
from pygame.math import Vector2
from config import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, obstacleSprites):
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.direction = Vector2()
        self.obstacleSprites = obstacleSprites

    def __getattr__(self, _):
        return None

    # 移动
    def move(self, speed, stopMove=False):
        if not stopMove:
            self.hitbox.x += self.direction.x * speed
            self.collision("horizontal")
            self.hitbox.y += self.direction.y * speed
            self.collision("vertical")
            self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox) and sprite != self:
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox) and sprite != self:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
