import pygame
from config import *


class UI:
    def __init__(self, imgList, startTime):
        # general
        self.displaySurface = pygame.display.get_surface()
        self.imgList = imgList
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        # pygame.time.get_ticks()
        # bar setup
        self.gridSize = SCALE_RATE * 8
        self.startTime = startTime
        halfScreenWidth = self.displaySurface.get_size()[0] // 2
        self.barOffsetX = halfScreenWidth - TIME_BAR_WIDTH // 2 - self.gridSize // 2
        self.time_bar_rect = pygame.Rect(
            self.barOffsetX + 10 + self.gridSize, 32, TIME_BAR_WIDTH, BAR_HEIGHT
        )

    # 游戏时间
    def show_bar(self, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, bg_rect)

        # drawing the bar
        current = TOTAL_TIME - pygame.time.get_ticks() + self.startTime
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        currentRect = bg_rect.copy()
        currentRect.width = current_width

        self.displaySurface.blit(self.imgList[1], (self.barOffsetX - 10, 24))
        pygame.draw.rect(self.displaySurface, color, currentRect)

    # 用户血量
    def draw_health_bar(self, current, max_amount, blank, exist, offset):
        (offsetX, offsetY) = offset
        healthList = []
        for hl in range(max_amount):
            if hl < current:
                healthList.append((exist, (offsetX + hl * 16 * SCALE_RATE, offsetY)))
            else:
                healthList.append((blank, (offsetX + hl * 16 * SCALE_RATE, offsetY)))
            self.displaySurface.blits(healthList)

    # 用户得分
    def show_score(self, score):
        text = self.font.render("score:", False, "black")
        text_surf = self.font.render(str(int(score)), False, "black")
        x1 = self.displaySurface.get_size()[0] - 100
        x2 = self.displaySurface.get_size()[0]
        y = 32
        text_rect = text.get_rect(topright=(x1, y))
        text_surf_rect = text.get_rect(topright=(x2, y))

        self.displaySurface.blits(
            blit_sequence=((text, text_rect), (text_surf, text_surf_rect))
        )

    # 展示
    def display(self, player):
        self.draw_health_bar(
            player.health, MAX_HEALTH, self.imgList[0], self.imgList[2], (10, 10)
        )
        self.show_bar(TOTAL_TIME, self.time_bar_rect, TIME_COLOR)
        self.show_score(player.score)
        # pygame.draw.rect(self.displaySurface,'red',self.health_bar_rect)

