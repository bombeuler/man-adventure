import pygame
from config import *


class AnimationSprite(pygame.sprite.Sprite):
    def __init__(
        self, pos, groups, imageList, animationSpeed=0.15, spriteType="staticbody"
    ):
        super().__init__(groups)
        self.imageList = imageList
        self.image = imageList[0]
        self.spriteType = spriteType
        self.frameIndex = 0
        self.animationSpeed = animationSpeed
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -6 * SCALE_RATE)

    def __getattr__(self, _):
        return None

    def animate(self):
        # 动画loop
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.imageList):
            self.frameIndex = 0

        # 设置图片
        self.image = self.imageList[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self, dt):
        self.animate()
