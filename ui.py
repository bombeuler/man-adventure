import pygame
# from settings import *

class UI:
    def __init__(self):
        #general
        self.display_surface=pygame.display.get_surface()
        self.font=pygame.font.Font(UI_FONT,)

    def display(self,player):
        pass