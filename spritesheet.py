import pygame
from jsonconvert import JSONConvert
from config import *


class SpriteSheet:
    def __init__(self, sheetName):
        sheetPath = f'{ASSETS_PATH}/{sheetName}.png'
        self.sheet = pygame.image.load(sheetPath).convert_alpha()
        self.data = JSONConvert(sheetName)
        # print(f'无法加载图片{sheetName}')
        # print(pygame.error)

    def __cut_one(self, rect, scale):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        (_, _, w, h) = rect
        image = pygame.transform.scale(image, (scale * w, scale * h))
        return image

    def loop_img(self, name, scale=1):
        rectLists = self.data.query(name)
        img_list = []
        for rect in rectLists:
            img_list.append(self.__cut_one(rect, scale))
        return img_list