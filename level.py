import pygame
from pygame.math import Vector2
from math import exp
from config import *
from spritesheet import SpriteSheet
from player import Player
from tile import Tile
from tilemap import TileMap
from animationSprite import AnimationSprite
from enemy import Enemy
from random import random
from ui import UI


class Level:
    def __init__(self):
        # 获取显示表面
        self.displaySurface = pygame.display.get_surface()
        self.basicSheet = SpriteSheet("basic_sheet")
        self.gameStatus = "run"

        # 音乐
        self.bgm = pygame.mixer.Sound(f"{ASSETS_PATH}/bgm.ogg")
        self.bgm.set_volume(0.2)

        # 储存怪物列表
        self.monosterImages = {}
        for k, _ in monosterData.items():
            if k == "dragon":
                self.monosterImages[k] = self.basicSheet.loop_img(k, 2 * SCALE_RATE)
            else:
                self.monosterImages[k] = self.basicSheet.loop_img(k, SCALE_RATE)

        self.hurtImages = self.basicSheet.loop_img("hurt_action", SCALE_RATE)
        self.greenDeadImg = self.basicSheet.loop_img("enemy_dead", SCALE_RATE)
        self.redDeadImg = self.basicSheet.loop_img("redead", SCALE_RATE)
        self.dragonDeadImg = self.basicSheet.loop_img("redead", 2 * SCALE_RATE)
        self.whiteImg = self.basicSheet.loop_img("movebroad", SCALE_RATE)
        self.uiImg = self.basicSheet.loop_img("player_status", SCALE_RATE)
        self.itemImg = self.basicSheet.loop_img("buff", SCALE_RATE)

        # 精灵组
        self.visibleSprites = YSortCameraGroup()  # 可视组
        self.obstaclesSprites = pygame.sprite.Group()  # 物理碰撞
        self.hurtingSprites = pygame.sprite.Group()  # 造成伤害
        self.hurtSprites = pygame.sprite.Group()  # 受到伤害
        self.itemSprites = pygame.sprite.Group()  # 道具组

        # 精灵初始化
        self.create_map()
        self.startTime = pygame.time.get_ticks()
        self.spawnTime = pygame.time.get_ticks()
        self.bgm.play()

        # 用户界面
        self.ui = UI(self.uiImg, self.startTime)

    # 初始化地图
    def create_map(self):
        # 导入图片地图等资源
        thingMap = TileMap("things").get_map()
        bgImg = self.basicSheet.loop_img("background", SCALE_RATE)
        playerImg = self.basicSheet.loop_img("player", SCALE_RATE)

        # 绘制碰撞静止物体
        for rowIndex, row in enumerate(thingMap):
            for colIndex, col in enumerate(row):
                if col != "-1":
                    x = colIndex * TILESIZE
                    y = rowIndex * TILESIZE
                    if col == "71":
                        AnimationSprite(
                            (x, y),
                            [self.obstaclesSprites, self.visibleSprites],
                            bgImg[5:7],
                            0.05,
                        )
                    elif col == "73":
                        Tile(
                            (x, y),
                            [self.obstaclesSprites, self.visibleSprites],
                            bgImg[7],
                        )
                    elif col == "76":
                        Tile(
                            (x, y),
                            [self.obstaclesSprites, self.visibleSprites],
                            bgImg[10],
                        )

        # 绘制玩家

        self.player = Player(
            (SCALE_RATE * 1600, SCALE_RATE * 1600),
            [self.visibleSprites, self.hurtSprites, self.obstaclesSprites],
            self.obstaclesSprites,
            [self.visibleSprites, self.hurtingSprites],
            playerImg,
        )

    # 生成怪物

    def spawn_enemy(self):
        nowTime = pygame.time.get_ticks()
        # 胜利
        if nowTime - self.startTime >=TOTAL_TIME:
            self.gameStatus = "win"
        totalEnemy = 35
        spawnEnemy = max(int(exp(2 * (nowTime - self.startTime) / TOTAL_TIME)), 2)
        if (
            len(
                [
                    sprites
                    for sprites in self.hurtingSprites
                    if sprites.spriteType == "enemy"
                ]
            )
            >= totalEnemy
        ):
            return
        timeInterval = 2000 / spawnEnemy
        if nowTime - self.spawnTime >= timeInterval and spawnEnemy:
            enemySeed = 100 * random()
            posXSeed = 1600 * (random() - 0.5)
            posYSeed = 1600 * (random() - 0.5)
            enemyName = self.choose_enemy(nowTime, enemySeed)
            playerPos = self.player.rect.center
            enemyPosX = (
                posXSeed + 800 if posXSeed > 0 else posXSeed - 800
            ) + playerPos[0]
            enemyPosY = (
                posYSeed + 800 if posYSeed > 0 else posYSeed - 800
            ) + playerPos[1]
            enemyPos = (enemyPosX, enemyPosY)
            if enemyName == "creeper":
                Enemy(
                    "creeper",
                    self.player,
                    self.monosterImages,
                    self.greenDeadImg,
                    self.itemImg,
                    enemyPos,
                    [self.visibleSprites, self.hurtSprites, self.hurtingSprites],
                    self.obstaclesSprites,
                    [self.visibleSprites, self.itemSprites],
                )
            elif enemyName == "bat":
                Enemy(
                    "bat",
                    self.player,
                    self.monosterImages,
                    self.redDeadImg,
                    self.itemImg,
                    enemyPos,
                    [self.visibleSprites, self.hurtSprites, self.hurtingSprites],
                    self.obstaclesSprites,
                    [self.visibleSprites, self.itemSprites],
                )
            elif enemyName == "turtle":
                Enemy(
                    "turtle",
                    self.player,
                    self.monosterImages,
                    self.greenDeadImg,
                    self.itemImg,
                    enemyPos,
                    [self.visibleSprites, self.hurtSprites, self.hurtingSprites],
                    self.obstaclesSprites,
                    [self.visibleSprites, self.itemSprites],
                )
            else:
                Enemy(
                    "dragon",
                    self.player,
                    self.monosterImages,
                    self.dragonDeadImg,
                    self.itemImg,
                    enemyPos,
                    [self.visibleSprites, self.hurtSprites, self.hurtingSprites],
                    self.obstaclesSprites,
                    [self.visibleSprites, self.itemSprites],
                )

            self.spawnTime = nowTime

    # 怪物选择区段
    def choose_enemy(self, nowTime, seed):
        firstSheet = (70, 15, 13)
        lastSheet = (
            25,
            45,
            20,
        )
        rate = (nowTime - self.startTime) / TOTAL_TIME
        e1 = firstSheet[0] + (lastSheet[0] - firstSheet[0]) * rate
        e2 = firstSheet[1] + (lastSheet[1] - firstSheet[1]) * rate
        e3 = firstSheet[2] + (lastSheet[2] - firstSheet[2]) * rate
        if seed <= e1:
            return "creeper"
        elif seed <= e1 + e2:
            return "bat"
        elif seed <= e1 + e2 + e3:
            return "turtle"
        else:
            return "dragon"

    # 攻击与被攻击逻辑
    def hurt_hurting_logic(self):
        if self.hurtingSprites:
            for hurtingSprite in self.hurtingSprites:
                collisionSprites = pygame.sprite.spritecollide(
                    hurtingSprite, self.hurtSprites, False
                )
                if collisionSprites:
                    for targetSprite in collisionSprites:
                        if targetSprite.spriteType != hurtingSprite.origin.spriteType:
                            self.damage_judge(hurtingSprite, targetSprite)

    # 伤害判定
    def damage_judge(self, hurtingSprite, targetSprite):
        damage = hurtingSprite.damage
        nowHealth = targetSprite.health
        if damage >= nowHealth:
            self.hurtSprites.remove(targetSprite)
            targetSprite.health = 0
            if monosterData.get(targetSprite.name):
                self.player.score += monosterData.get(targetSprite.name)["score"]
            elif targetSprite.name == "player":
                self.gameStatus = "lost"
            targetSprite.set_status("death", self.hurtingSprites)
        else:
            targetSprite.health = nowHealth - damage
            if targetSprite.spriteType == "player":
                targetSprite.set_status(
                    "hurt", (self.hurtSprites, pygame.time.get_ticks())
                )
        if hurtingSprite.once:
            hurtingSprite.kill()

    def run(self, dt):
        self.visibleSprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.spawn_enemy()
        self.visibleSprites.update(dt)
        self.visibleSprites.enemy_update(self.player)
        self.visibleSprites.item_update(self.player)
        self.hurt_hurting_logic()
        


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # 绘制背景并且让背景符合摄像机
        background = pygame.image.load(f"{ASSETS_PATH}/background.png").convert_alpha()
        bgX = background.get_rect().w
        bgY = background.get_rect().h
        self.background = pygame.transform.scale(
            background, (SCALE_RATE * bgX, SCALE_RATE * bgY)
        )

        self.bgRect = self.background.get_rect(topleft=(0, 0))

        # 让可视组符合摄像机
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0] // 2
        self.halfHeight = self.displaySurface.get_size()[1] // 2
        self.offset = Vector2()

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        bgOffsetPos = self.bgRect.topleft - self.offset
        self.displaySurface.blit(self.background, bgOffsetPos)

        for sprite in self.sort_by(self.sprites()):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPos)

    def sort_by(self, sprites):
        sorted1 = sorted(sprites, key=lambda sprite: sprite.rect.centery)
        sorted2 = sorted(sorted1, key=lambda sprite: 1 if sprite.fly else 0)
        sorted3 = sorted(sorted2, key=lambda sprite: spriteOrder.get(sprite.spriteType))

        return sorted3

    def enemy_update(self, player):
        enemySprites = [
            sprite for sprite in self.sprites() if sprite.spriteType == "enemy"
        ]
        for enemy in enemySprites:
            enemy.enemy_update(player)

    def item_update(self, player):
        itemSprites = [
            sprite for sprite in self.sprites() if sprite.spriteType == "item"
        ]
        if itemSprites:
            for item in itemSprites:
                item.item_update(player)
