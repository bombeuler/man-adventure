import pygame
from config import *
from jsonconvert import JSONConvert
from spritesheet import SpriteSheet
from player import Player
from tile import Tile

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
        img_list = self.basicSheet.loop_img('background',2)
        for row_index,row in enumerate(WORLD_MAP):
            for col_index ,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
            match col :
                case 'x':
                    Tile((x,y),[self.visible_sprites],img_list[5])

    def run(self, dt):
        self.display_surface.fill("black")
        self.visible_sprites.draw(self.display_surface)
        # self.all_sprites.update(dt)