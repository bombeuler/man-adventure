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
        self.backgroundSprites = BackgroundGroup()
        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        bgMap = TileMap('background').get_map()
        thingMap = TileMap('things').get_map()
        bgImg = self.basicSheet.loop_img('background',SCALE_RATE)
        playerImg = self.basicSheet.loop_img('player',SCALE_RATE)

        # for rowIndex,row in enumerate(WORLD_MAP):
        #     for colIndex ,grid in enumerate(row):
        #         x = colIndex * TILESIZE
        #         y = rowIndex * TILESIZE
        #         match grid :
        #             case 'x':
        #                 Tile((x,y),[self.visibleSprites,self.obstaclesSprites],bgImg[6])
        #             case ' ':
        #                 Tile((x,y),[self.backgroundSprites],bgImg[3])
        
        # self.player = Player((600,100),[self.visibleSprites],self.obstaclesSprites,playerImg[2])

        # 绘制背景
        for rowIndex,row in enumerate(bgMap):
            for colIndex ,col in enumerate(row):
                if col !=-1:
                    x = colIndex * TILESIZE
                    y = rowIndex * TILESIZE
                    match col :
                        case '66':
                            Tile((x,y),[self.backgroundSprites],bgImg[0])
                        case '67':
                            Tile((x,y),[self.backgroundSprites],bgImg[1])
                        case '68':
                            Tile((x,y),[self.backgroundSprites],bgImg[2])
                        case '69':
                            Tile((x,y),[self.backgroundSprites],bgImg[3])
                        case '70':
                            Tile((x,y),[self.backgroundSprites],bgImg[4])

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
        
        self.player = Player((400,400),[self.obstaclesSprites,self.visibleSprites],self.obstaclesSprites,playerImg[2])

    def run(self, dt):
        self.backgroundSprites.custom_draw(self.player)
        self.visibleSprites.custom_draw(self.player)
        self.visibleSprites.update(dt)
        debug(self.player.rect)

class BackgroundGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0]//2
        self.halfHeight = self.displaySurface.get_size()[1]//2
        self.offset = Vector2()

    def custom_draw(self,player):

        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image,offsetPos)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0]//2
        self.halfHeight = self.displaySurface.get_size()[1]//2
        self.offset = Vector2()

    def custom_draw(self,player):

        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image,offsetPos)