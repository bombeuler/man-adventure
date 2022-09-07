import pygame
from random import random
from config import *
from entity import Entity
from pygame.math import Vector2
from debug import debug


class Enemy(Entity):
    def __init__(
        self,
        moster_name,
        player,
        monosterImage,
        deadImage,
        pos,
        groups,
        obstacleSprites,
    ):
        super().__init__(groups, obstacleSprites)
        self.animationSpeed = 0.1
        self.animationKind = "alive"
        self.spriteType = "enemy"
        self.name = moster_name
        self.player = player
        self.origin = self
        # 导入数据
        self.import_data()

        self.imageList = monosterImage.get(self.name)
        self.deadImage = deadImage
        self.image = self.imageList[0]
        self.rect = self.image.get_rect(center=pos)

        # 设置碰撞箱
        self.set_hitbox()

    # 设置碰撞箱
    def set_hitbox(self):
        if self.fly:
            self.hitbox = self.rect.inflate(-12 * SCALE_RATE, -12 * SCALE_RATE)
        else:
            self.hitbox = self.rect.inflate(0, -6 * SCALE_RATE)

    # 导入数据
    def import_data(self):
        data = monosterData.get(self.name)
        self.once = False
        self.stopMove = False
        self.remainTime = 0
        self.health = data["health"]
        self.speed = data["speed"]
        self.damage = data["damage"]
        self.fly = data["fly"]

    # 获取玩家状态
    def get_status(self, player):
        enemyVec = Vector2(self.rect.center)
        playerVec = Vector2(player.rect.center)
        distance = (playerVec - enemyVec).magnitude()

        # 设置运行方向
        if distance > 10:
            self.direction = (playerVec - enemyVec).normalize()
        else:
            self.direction = Vector2()

    # 飞行怪物特别移动方式
    def fly_move(self, speed, stopMove=False):
        if not stopMove:
            self.hitbox.x += self.direction.x * speed
            self.hitbox.y += self.direction.y * speed
            self.rect.center = self.hitbox.center

    def animate(self, dt):
        # 正常动画loop
        if self.animationKind == "alive":
            self.frameIndex += self.animationSpeed
            if self.frameIndex >= len(self.imageList):
                self.frameIndex = 0
            # 设置图片
            self.image = self.imageList[int(self.frameIndex)]
            self.rect = self.image.get_rect(center=self.hitbox.center)
        else:
            self.frameIndex += self.animationSpeed
            if self.frameIndex >= len(self.deadImage):
                self.frameIndex = len(self.deadImage) - 1
            # 设置图片
            self.image = self.deadImage[int(self.frameIndex)]
            self.rect = self.image.get_rect(center=self.hitbox.center)

    def set_status(self, signal, information):
        if signal == "death":
            self.remove(information)
            self.stopMove = True
            self.animationKind = "dead"

    def loop_status(self):
        if self.animationKind == "dead":
            self.remainTime += 1
        if self.remainTime >= 100:
            self.kill()

    def update(self, dt):
        if self.fly:
            self.fly_move(self.speed, self.stopMove)
        else:
            self.move(self.speed, self.stopMove)
        self.animate(dt)
        self.loop_status()

    def enemy_update(self, player):
        self.get_status(player)
