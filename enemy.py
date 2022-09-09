import pygame
from random import random, randint
from config import *
from entity import Entity
from pygame.math import Vector2
from item import Item


class Enemy(Entity):
    def __init__(
        self,
        moster_name,
        player,
        monosterImage,
        deadImage,
        itemImage,
        pos,
        groups,
        obstacleSprites,
        itemGroups,
    ):
        super().__init__(groups, obstacleSprites)
        self.animationSpeed = 0.1
        self.animationKind = "alive"
        self.spriteType = "enemy"
        self.name = moster_name
        self.player = player
        self.origin = self
        self.itemGroups = itemGroups
        self.itemImage = itemImage
        # 导入数据
        self.import_data()
        if self.name == "turtle":
            self.imageList = monosterImage.get(self.name)[0:2]
        else:
            self.imageList = monosterImage.get(self.name)
        self.deadImage = deadImage
        self.image = self.imageList[0]
        self.rect = self.image.get_rect(center=pos)

        self.deadSound = pygame.mixer.Sound(f"{ASSETS_PATH}/shooted.ogg")
        self.deadSound.set_volume(0.25)

        # 设置碰撞箱
        self.set_hitbox()

    # 设置碰撞箱
    def set_hitbox(self):
        if self.fly:
            self.hitbox = self.rect.inflate(-6 *SCALE_RATE, -6 * SCALE_RATE)
        else:
            self.hitbox = self.rect.inflate(-6 * SCALE_RATE, -12 * SCALE_RATE)

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
    def fly_move(self, speed, dt, stopMove=False):
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
            self.deadSound.play()
            self.remove(information)
            self.stopMove = True
            self.animationKind = "dead"

    def loop_status(self):
        if self.animationKind == "dead":
            self.remainTime += 1
        if self.remainTime >= 60:
            haveItemSeed = random()
            if haveItemSeed <= ITEM_PROBABLY:
                itemSeed = randint(1, WEIGHT_ALL)
                offset = 0
                for k, item in effectData.items():
                    weight = item["weight"]
                    if itemSeed <= offset + weight:
                        effectName = k
                        imgIndex = item['imageIndex']
                        break
                    else:
                        offset += weight

                Item(self.rect.center, self.itemGroups, self.itemImage[imgIndex], effectName)
            self.kill()

    def update(self, dt):
        if self.fly:
            self.fly_move(self.speed, dt, self.stopMove)
        else:
            self.move(self.speed, dt, self.stopMove)
        self.animate(dt)
        self.loop_status()

    def enemy_update(self, player):
        self.get_status(player)
