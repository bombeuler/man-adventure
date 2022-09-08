from distutils import text_file
import pygame
from config import *

class Menu:
    def __init__(self) :
        self.displaySurface=pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.bigFont = pygame.font.Font(UI_FONT,30) 
    #开始界面 & 结束界面
    def show_start(self):
        # self.displaySurface.blit(bg, (0,0))
        gameTitle = self.bigFont.render("荒漠求生",False, 'white')
        text=self.font.render("开始游戏", False, 'yellow')

        self.displaySurface.blit(gameTitle, (self.displaySurface.get_size()[0] // 2 - gameTitle.get_width()//2, 150))
        self.displaySurface.blit(text, (self.displaySurface.get_size()[0] // 2 - text.get_width()//2,400))
    
    def show_success(self):
        
        successBg = self.bigFont.render("你活了下来!",False, 'yellow')
        text=self.font.render("重新开始", False, 'yellow')

        self.displaySurface.blit(successBg, (self.displaySurface.get_size()[0] // 2 - successBg.get_width()//2, 150))
        self.displaySurface.blit(text, (self.displaySurface.get_size()[0] // 2 - text.get_width()//2,400))
    
    def show_lost(self):
        lostBg=self.bigFont.render("你已被杀死...", False, 'red')
        text=self.font.render("重新开始", False, 'yellow')
        
        self.displaySurface.blit(lostBg, (self.displaySurface.get_size()[0] // 2 - lostBg.get_width()//2, 150))
        self.displaySurface.blit(text, (self.displaySurface.get_size()[0] // 2 - text.get_width()//2,400))

    def show_score(self, score):
        text = self.font.render("分数：", False, "white")
        text_surf = self.font.render(str(int(score)), False, "white")
        x1= self.displaySurface.get_size()[0] // 2 - text.get_width()//2
        x2= self.displaySurface.get_size()[0] // 2 + text.get_width()*1.5
        text_rect = text.get_rect(topright=(x1, 250))
        text_surf_rect = text.get_rect(topright=(x2, 250))

        self.displaySurface.blits(
            blit_sequence=((text, text_rect), (text_surf, text_surf_rect))
        )


    def display(self,signal,score):
        self.displaySurface.fill('black')
        if signal=='start':
            self.show_start()
        elif signal=='win':
            self.show_success()
            self.show_score(score)
        else:
            self.show_lost()
            self.show_score(score)

