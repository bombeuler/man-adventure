import pygame
from config import *
from spritesheet import SpriteSheet
from player import Player
from tile import Tile
from debug import debug


class Level:
    def __init__(self):
        # 获取显示表面
        self.display_surface = pygame.display.get_surface()
        self.basicSheet = SpriteSheet('basic_sheet')

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        bgImg = self.basicSheet.loop_img('background',2)
        playerImg = self.basicSheet.loop_img('player',2)
        for row_index,row in enumerate(WORLD_MAP):
            for col_index ,grid in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                match grid :
                    case 'x':
                        Tile((x,y),[self.visible_sprites],bgImg[6])
                    case 'p':
                        self.player = Player((x,y),[self.visible_sprites],playerImg[2])

    def run(self, dt):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(dt)
        debug(len(self.visible_sprites))