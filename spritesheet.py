import pygame
from jsonconvert import JSONConvert
from config import *
from pygame.locals import SRCALPHA
from debug import debug

class SpriteSheet:
    def __init__(self, sheetName):
        sheetPath = f'{ASSETS_PATH}/{sheetName}.png'
        sheetImage = pygame.image.load(sheetPath).convert_alpha()
        # sheetImage.set_colorkey(pygame.Color(0,0,0,255))
        self.sheet = sheetImage
        self.data = JSONConvert(sheetName)
        # print(f'无法加载图片{sheetName}')
        # print(pygame.error)

    def __cut_one(self, rect, scale):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size,SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        (_, _, w, h) = rect
        image = pygame.transform.scale(image,
                                       (scale * w, scale * h))
        return image

    def loop_img(self, name, scale=2):
        rectLists = self.data.query(name)
        img_list = []
        for rect in rectLists:
            img_list.append(self.__cut_one(rect, scale))
        return img_list