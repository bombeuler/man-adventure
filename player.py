import pygame
from pygame.math import Vector2
from config import *
from bullet import Bullet
from entity import Entity
from pygame.locals import SRCALPHA


class Player(Entity):
    def __init__(self, pos, group, obstacleSprites, bulletSprites, imageList):
        super().__init__(group, obstacleSprites)

        # 基本属性
        self.spriteType = "player"
        self.imageList = imageList
        self.body = self.imageList[2]
        self.name = "player"

        legList = []
        for i in range(4):
            rect = pygame.Rect((0, 3 * i * SCALE_RATE, 16 * SCALE_RATE, 3 * SCALE_RATE))
            leg = pygame.Surface(rect.size, SRCALPHA).convert_alpha()
            leg.blit(self.imageList[0], (0, 0), rect)
            legList.append(leg)
        self.legs = legList
        self.leg = self.legs[2]
        print(legList[0])

        # 连接身子跟腿
        self.draw_player(self.body, self.leg)
        self.legFrameIndex = 0
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-6, -6 * SCALE_RATE)

        # 状态和动画
        self.status = {"face": "down", "shootFace": "down", "display": "idle"}
        self.pos = Vector2(self.hitbox.center)

        # 声音
        self.shootSound = pygame.mixer.Sound(f"{ASSETS_PATH}/shoot.ogg")
        self.shootSound.set_volume(0.25)
        self.hurtSound = pygame.mixer.Sound(f"{ASSETS_PATH}/hurt.ogg")
        self.hurtSound.set_volume(0.25)

        # 用户属性
        self.speed = PLAYER_MINSPEED  # 移动速度
        self.shootingCooldown = MAX_COLDDOWN  # 子弹冷却
        self.bulletSpeed = BULLET_MINSPEED  # 子弹飞行速度
        self.health = MAX_HEALTH  # 生命值
        self.bulletDamage = 1
        self.stopHurt = False
        self.hurtTime = 0
        self.score = 0

        # 射击
        self.shootDirection = Vector2()
        self.shooting = False
        self.fiveBullets = 5
        self.bigBullets = 3

        self.shootTime = None

        self.bulletSprites = bulletSprites

    def draw_player(self, body, leg):
        image = pygame.Surface(
            (16 * SCALE_RATE, 16 * SCALE_RATE), SRCALPHA
        ).convert_alpha()
        image.blits([(body, (0, 0)), (leg, (0, 13 * SCALE_RATE))])
        self.image = image

    def get_animation_key(self, status):
        if self.shooting:
            decide = "shootFace"
        else:
            decide = "face"

        if status[decide] == "up":
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
        if self.bigBullets > 0:
            self.bigBullets -=1
            Bullet(
                True,
                self.bulletSprites,
                (x, y),
                3,
                self.bulletDamage,
                self.shootDirection,
                self,
            )
            if self.fiveBullets > 0:
                self.fiveBullets -= 1
                self.shootfive(x, y,True,3)
        else:
            Bullet(
                False,
                self.bulletSprites,
                (x, y),
                speed,
                self.bulletDamage,
                self.shootDirection,
                self,
            )
            if self.fiveBullets > 0:
                self.fiveBullets -= 1
                self.shootfive(x, y,False,speed)

    # 三枪射击状态
    def shootfive(self, x, y, is_big,speed):
        if is_big:
            rotateDegree = 30
        else:
            rotateDegree = 20
        directionl1 = self.shootDirection.rotate(-rotateDegree)
        directionr1 = self.shootDirection.rotate(rotateDegree)
        directionl2 = self.shootDirection.rotate(-2*rotateDegree)
        directionr2 = self.shootDirection.rotate(2*rotateDegree)
        for direction in [directionl1, directionl2, directionr1, directionr2]:
            Bullet(
                is_big,
                self.bulletSprites,
                (x, y),
                speed,
                self.bulletDamage,
                direction,
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
        self.body = self.imageList[key]

        # 腿的动画
        if self.status["display"] != "idle":
            self.legFrameIndex += self.animationSpeed
            if self.legFrameIndex >= 4:
                self.legFrameIndex = 0
        self.leg = self.legs[int(self.legFrameIndex)]

        self.draw_player(self.body, self.leg)
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
        self.move(self.speed, dt)
