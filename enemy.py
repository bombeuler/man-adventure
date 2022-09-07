from xml.dom.minidom import Entity
import pygame
from config import *
from entity import Entity
from pygame.math import Vector2
from debug import debug

class Enemy(Entity):
    def __init__(self,moster_name,player,monosterImage,pos,groups,obstacleSprites):
        super().__init__(groups,obstacleSprites)
        self.animationSpeed = 0.1
        self.spriteType = 'enemy'
        self.name = moster_name
        self.player = player
        # 导入数据
        self.import_data()

        self.imageList = monosterImage.get(self.name)
        self.image = self.imageList[0]
        self.rect = self.image.get_rect(center = pos)


        # 设置碰撞箱
        self.set_hitbox()

        # 移动
    
    # 设置碰撞箱
    def set_hitbox(self):
        if self.fly:
            self.hitbox = self.rect.inflate(-12 * SCALE_RATE, -12 * SCALE_RATE)
        else:
            self.hitbox = self.rect.inflate(0, -6 * SCALE_RATE)


    # 导入数据
    def import_data(self):
        data = monosterData.get(self.name)
        self.health = data['health']
        self.speed = data['speed']
        self.damage = data['damage']
        self.fly = data['fly']
    
    def get_direction(self):
        self.direction = Vector2((self.player.rect.x -self.rect.x,self.player.rect.y - self.rect.y)).normalize()

    def fly_move(self,speed):
        self.hitbox.x += self.direction.x * speed
        self.hitbox.y += self.direction.y * speed
        self.rect.center = self.hitbox.center

    def animate(self):
        # 动画loop
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.imageList):
            self.frameIndex = 0

        # 设置图片
        self.image = self.imageList[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self,dt):
        self.get_direction()
        if self.fly:
            self.fly_move(self.speed)
        else:
            self.move(self.speed)
        debug(self.direction)
        self.animate()

