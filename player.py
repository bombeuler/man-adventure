import pygame
from pygame.math import Vector2
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, obstacleSprites,image):
        super().__init__(group)

        # 基本属性
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0,-6 * SCALE_RATE)

        # 物理属性
        self.direction = Vector2((0, 0))
        self.pos = Vector2(self.hitbox.center)
        self.speed = PLAYER_MAXSPEED

        self.obstacleSprites = obstacleSprites

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
        if directionVector.magnitude() !=0:
            directionVector = directionVector.normalize()
        self.direction = directionVector

    # 玩家移动
    def move(self, speed):
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    # 玩家碰撞
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox) and sprite !=self:
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox) and sprite !=self:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self, dt):
        self.input()
        self.move(self.speed)