import pygame
from pygame.math import Vector2
from config import *


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image, effect):
        super().__init__(groups)
        self.image = image
        self.spriteType = "item"
        self.rect = self.image.get_rect(topleft=pos)
        self.effect = effect

    def get_status(self, player):
        itemVec = Vector2(self.rect.center)
        playerVec = Vector2(player.rect.center)
        distance = (playerVec - itemVec).magnitude()
        if distance <= 10 * SCALE_RATE:
            self.change_status(player)

    def item_update(self, player):
        self.get_status(player)

    def __getattr__(self, _):
        return None

    def change_status(self, player):
        itemData = effectData.get(self.effect)
        if itemData.get("type") == "simple":
            attributeName = itemData.get("influence")[0]
            valuechanged = itemData.get("influence")[1]
            minboarder = itemData.get("influence")[2]
            maxboarder = itemData.get("influence")[3]
            changedResult = round(getattr(player, attributeName) + valuechanged, 1)
            if changedResult >= minboarder and changedResult <= maxboarder:
                setattr(player, attributeName, changedResult)
        elif self.effect == "fiveBullets":
            player.fiveBullets = itemData["lastTime"]
        elif self.effect == "bigBullets":
            player.bigBullets = itemData['lastTime']
        self.kill()
