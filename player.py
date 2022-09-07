import pygame
from pygame.math import Vector2
from config import *
from bullet import Bullet
from entity import Entity


class Player(Entity):
    def __init__(self, pos, group, obstacleSprites, bulletSprites,imageList):
        super().__init__(group,obstacleSprites)

        # 基本属性
        self.spriteType = 'player'
        self.imageList = imageList
        self.image = self.imageList[2]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -6 * SCALE_RATE)

        # 状态和动画
        self.status = {'face': 'down', 'display': 'idle'}

        # 物理属性
        self.pos = Vector2(self.hitbox.center)
        self.speed = PLAYER_MAXSPEED

        # 射击
        self.shootDirection = Vector2()
        self.shooting = False
        self.shootingCooldown = 400
        self.bulletSpeed = BULLET_MINSPEED
        self.shootTime = None

        self.bulletSprites = bulletSprites


    def get_animation_key(self,status):
        match status['face']:
            case 'up':
                return 1
            case 'right':
                return 2
            case 'down':
                return 3
            case 'left':
                return 4


    # 用户按键操作
    def input(self):
        keys = pygame.key.get_pressed()

        # 玩家移动指令
        directionVector = Vector2()
        if keys[pygame.K_UP]:
            directionVector.y -= 1
            self.status['face'] = 'up'
            self.status['display'] = 'run'
        elif keys[pygame.K_DOWN]:
            directionVector.y += 1
            self.status['face'] = 'down'
            self.status['display'] = 'run'

        if keys[pygame.K_LEFT]:
            directionVector.x -= 1
            self.status['face'] = 'left'
            self.status['display'] = 'run'
        elif keys[pygame.K_RIGHT]:
            directionVector.x += 1
            self.status['face'] = 'right'
            self.status['display'] = 'run'

        if directionVector.magnitude() != 0:
            directionVector = directionVector.normalize()
        self.direction = directionVector

        # 玩家攻击指令
        if not self.shooting and (keys[pygame.K_a] or keys[pygame.K_d]
                                  or keys[pygame.K_w] or keys[pygame.K_s]):
            self.shooting = True
            self.shootTime = pygame.time.get_ticks()
            shootVector = Vector2()
            if keys[pygame.K_a]:
                shootVector.x -= 1
                self.status['face'] = 'left'
            elif keys[pygame.K_d]:
                shootVector.x += 1
                self.status['face'] = 'right'

            if keys[pygame.K_w]:
                shootVector.y -= 1
                self.status['face'] = 'up'
            elif keys[pygame.K_s]:
                shootVector.y += 1
                self.status['face'] = 'down'
            if shootVector.magnitude() != 0:
                shootVector = shootVector.normalize()
            self.shootDirection = shootVector

            self.shoot(self.bulletSpeed)

    # 获取状态
    def get_status(self):

        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if self.status['display'] != 'idle':
                self.status['display'] = 'idle'

        # shoot
        if self.shooting:
            if self.status['display'] !='shoot':
                self.status['display'] = 'shoot'

    # 玩家射击
    def shoot(self,speed):
        x = self.rect.center[0] + 40*self.shootDirection.x
        y = self.rect.center[1] + 40*self.shootDirection.y
        Bullet(self.bulletSprites,(x,y),speed,self.shootDirection)

    # 射击冷却
    def cooldowns(self):
        currentTime = pygame.time.get_ticks()

        if self.shooting:
            if currentTime - self.shootTime >= self.shootingCooldown:
                self.shooting = False

    # 动画
    def animate(self):
        key = self.get_animation_key(self.status)


        # 动画loop
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= 1:
            self.frameIndex = 0

        # 设置图片
        self.image = self.imageList[key]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self, dt):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)