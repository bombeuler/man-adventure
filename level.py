import pygame
from pygame.math import Vector2
from config import *
from spritesheet import SpriteSheet
from player import Player
from tile import Tile
from debug import debug
from tilemap import TileMap
from animationSprite import AnimationSprite
from enemy import Enemy


class Level:
    def __init__(self):
        # 获取显示表面
        self.displaySurface = pygame.display.get_surface()
        self.basicSheet = SpriteSheet('basic_sheet')

        # 储存怪物列表
        self.monosterImages = {}
        for k,_ in monosterData.items():
            self.monosterImages[k]=self.basicSheet.loop_img(k,SCALE_RATE)

        self.hurtImages = self.basicSheet.loop_img('hurt_action',SCALE_RATE)

        # sprite groups
        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()
        self.startTime = pygame.time.get_ticks()
        self.spawnTime = pygame.time.get_ticks()

    def create_map(self):
        thingMap = TileMap('things').get_map()
        bgImg = self.basicSheet.loop_img('background',SCALE_RATE)
        playerImg = self.basicSheet.loop_img('player',SCALE_RATE)

        # 绘制碰撞静止物体
        for rowIndex,row in enumerate(thingMap):
            for colIndex ,col in enumerate(row):
                if col !='-1':
                    x = colIndex * TILESIZE
                    y = rowIndex * TILESIZE
                    match col :
                        case '71':
                            AnimationSprite((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[5:7],0.05)
                            # Tile((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[5])
                        case '73':
                            Tile((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[7])
                        case '76':
                            Tile((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[10])
        
        # 绘制玩家

        self.player = Player((SCALE_RATE*1600,SCALE_RATE*1600),[self.visibleSprites],self.obstaclesSprites,[self.visibleSprites],playerImg)

    def spawn_enemy(self):
        nowTime = pygame.time.get_ticks()
        timeInterval = 1500
        if nowTime - self.spawnTime >=timeInterval:
            Enemy('bat',self.player,self.monosterImages,(SCALE_RATE*1600,SCALE_RATE*1800),[self.visibleSprites],self.obstaclesSprites)
            self.spawnTime = nowTime


    def run(self, dt):
        self.spawn_enemy()
        self.visibleSprites.custom_draw(self.player)
        self.visibleSprites.update(dt)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # 绘制背景并且让背景符合摄像机
        background = pygame.image.load(f'{ASSETS_PATH}/background.png').convert_alpha()
        bgX = background.get_rect().w
        bgY = background.get_rect().h
        self.background = pygame.transform.scale(background,(SCALE_RATE * bgX,SCALE_RATE * bgY))

        self.bgRect = self.background.get_rect(topleft=(0,0))

        # 让可视组符合摄像机
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0]//2
        self.halfHeight = self.displaySurface.get_size()[1]//2
        self.offset = Vector2()

    def custom_draw(self,player):

        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        bgOffsetPos = self.bgRect.topleft - self.offset
        self.displaySurface.blit(self.background,bgOffsetPos)

        for sprite in self.sort_by(self.sprites()):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image,offsetPos)

    def sort_by(self,sprites):
        sorted1 = sorted(sprites,key = lambda sprite:sprite.rect.centery)
        sorted2 = sorted(sorted1,key = lambda sprite:1 if sprite.fly else 0)

        return sorted2