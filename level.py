import pygame
from pygame.math import Vector2
from config import *
from spritesheet import SpriteSheet
from player import Player
from tile import Tile
from debug import debug
from tilemap import TileMap


class Level:
    def __init__(self):
        # 获取显示表面
        self.displaySurface = pygame.display.get_surface()
        self.basicSheet = SpriteSheet('basic_sheet')
        # sprite groups
        self.visibleSprites = YSortCameraGroup()
        self.bulletSprites = pygame.sprite.Group()
        self.obstaclesSprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

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
                            Tile((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[5])
                        case '73':
                            Tile((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[7])
                        case '76':
                            Tile((x,y),[self.obstaclesSprites,self.visibleSprites],bgImg[10])
        
        # 绘制玩家

        self.player = Player((SCALE_RATE*1600,SCALE_RATE*1600),[self.obstaclesSprites,self.visibleSprites],self.obstaclesSprites,[self.bulletSprites,self.visibleSprites],playerImg)

    def run(self, dt):
        self.visibleSprites.custom_draw(self.player)
        self.visibleSprites.update(dt)
        self.bulletSprites.draw(self.displaySurface)
        self.bulletSprites.update(dt)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # 绘制背景并且让背景符合摄像机
        background = pygame.image.load(f'{ASSETS_PATH}/background.png').convert_alpha()
        bgX = background.get_rect().w
        bgY = background.get_rect().h
        self.background = pygame.transform.scale(background,(SCALE_RATE * bgX,SCALE_RATE *bgY))

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

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image,offsetPos)