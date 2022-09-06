import pygame
from config import *
from spritesheet import SpriteSheet
from player import Player
from tile import Tile
from debug import debug


class Level:
    def __init__(self):
        # 获取显示表面
        self.displaySurface = pygame.display.get_surface()
        self.basicSheet = SpriteSheet('basic_sheet')

        # sprite groups
        self.visibleSprites = pygame.sprite.Group()
        self.obstaclesSprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        bgImg = self.basicSheet.loop_img('background',2)
        playerImg = self.basicSheet.loop_img('player',2)
        for rowIndex,row in enumerate(WORLD_MAP):
            for colIndex ,grid in enumerate(row):
                x = colIndex * TILESIZE
                y = rowIndex * TILESIZE
                match grid :
                    case 'x':
                        Tile((x,y),[self.visibleSprites,self.obstaclesSprites],bgImg[6])
                    case ' ':
                        Tile((x,y),[self.visibleSprites],bgImg[3])
                    case 'p':
                        self.player = Player((x,y),[self.visibleSprites],self.obstaclesSprites,playerImg[2])

    def run(self, dt):
        self.visibleSprites.draw(self.displaySurface)
        self.visibleSprites.update(dt)
        debug(self.player.direction)