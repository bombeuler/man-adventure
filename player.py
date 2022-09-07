import pygame
from pygame.math import Vector2
from config import *
from bullet import Bullet
from entity import Entity


class Player(Entity):
    def __init__(self, pos, group, obstacleSprites, bulletSprites, imageList):
        super().__init__(group, obstacleSprites)

        # 基本属性
        self.spriteType = "player"
        self.imageList = imageList
        self.image = self.imageList[2]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-6, -6 * SCALE_RATE)

        # 状态和动画
        self.status = {"face": "down", "shootFace": "down", "display": "idle"}
        self.pos = Vector2(self.hitbox.center)

        # 声音
        self.shootSound = pygame.mixer.Sound(f'{ASSETS_PATH}/shoot.ogg')
        self.shootSound.set_volume(0.25)
        self.hurtSound = pygame.mixer.Sound(f'{ASSETS_PATH}/shooted.ogg')
        self.hurtSound.set_volume(0.25)

        # 用户属性
        self.speed = PLAYER_MAXSPEED  # 移动速度
        self.shootingCooldown = 400  # 子弹冷却
        self.bulletSpeed = BULLET_MINSPEED  # 射击速度
        self.health = 4  # 生命值
        self.bulletDamage = 1
        self.stopHurt = False
        self.hurtTime = 0

        # 射击
        self.shootDirection = Vector2()
        self.shooting = False

        self.shootTime = None

        self.bulletSprites = bulletSprites

    def get_animation_key(self, status):
        if self.shooting:
            decide = "shootFace"
        else:
            decide = "face"

        if status[decide] == 'up':
            return 1
        elif status[decide] == "right":
            return 2
        elif status[decide] == "down":
            return 3
        elif status[decide] == "left":
            return 4

    # 用户按键操作
    def input(self):
        keys = pygame.key.get_pressed()

        # 玩家移动指令
        directionVector = Vector2()
        if keys[pygame.K_w]:
            directionVector.y -= 1
            self.status["face"] = "up"
            self.status["display"] = "run"
        elif keys[pygame.K_s]:
            directionVector.y += 1
            self.status["face"] = "down"
            self.status["display"] = "run"

        if keys[pygame.K_a]:
            directionVector.x -= 1
            self.status["face"] = "left"
            self.status["display"] = "run"
        elif keys[pygame.K_d]:
            directionVector.x += 1
            self.status["face"] = "right"
            self.status["display"] = "run"

        if directionVector.magnitude() != 0:
            directionVector = directionVector.normalize()
        self.direction = directionVector

        # 玩家攻击指令
        if not self.shooting and (
            keys[pygame.K_UP]
            or keys[pygame.K_RIGHT]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_LEFT]
        ):
            self.shooting = True
            self.shootSound.play()
            self.shootTime = pygame.time.get_ticks()
            shootVector = Vector2()
            if keys[pygame.K_LEFT]:
                shootVector.x -= 1
                self.status["shootFace"] = "left"
            elif keys[pygame.K_RIGHT]:
                shootVector.x += 1
                self.status["shootFace"] = "right"

            if keys[pygame.K_UP]:
                shootVector.y -= 1
                self.status["shootFace"] = "up"
            elif keys[pygame.K_DOWN]:
                shootVector.y += 1
                self.status["shootFace"] = "down"
            if shootVector.magnitude() != 0:
                shootVector = shootVector.normalize()
            self.shootDirection = shootVector

            self.shoot(self.bulletSpeed)

    # 获取状态
    def get_status(self):
        nowTime = pygame.time.get_ticks()

        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if self.status["display"] != "idle":
                self.status["display"] = "idle"

        # shoot
        if self.shooting:
            if self.status["display"] != "shoot":
                self.status["display"] = "shoot"

        if self.stopHurt and nowTime - self.hurtTime > 1500:
            self.add(self.stopHurt)
            self.stopHurt = False

    # 玩家射击
    def shoot(self, speed):
        x = self.rect.center[0] + 20 * self.shootDirection.x
        y = self.rect.center[1] + 20 * self.shootDirection.y
        Bullet(
            self.bulletSprites,
            (x, y),
            speed,
            self.bulletDamage,
            self.shootDirection,
            self,
        )

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
        self.rect = self.image.get_rect(center=self.hitbox.center)

    # 死亡操作
    def set_status(self, signal, information):
        if signal == "hurt":
            self.hurtSound.play()
            self.stopHurt = information[0]
            self.remove(information[0])
            self.hurtTime = information[1]

    def update(self, dt):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed,dt)
