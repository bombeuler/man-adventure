import pygame, sys
from menu import Menu
from config import *
from level import Level
from pygame.locals import RESIZABLE, DOUBLEBUF, HWSURFACE


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)
        icon = pygame.image.load(f"{ASSETS_PATH}/icon.png").convert_alpha()
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.gameRun = False
        self.showMenu = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_SPACE and (not self.gameRun):
                        self.gameRun = True
                        self.showMenu = False
                        self.level = Level()
            # self.screen.fill("black")
            dt = self.clock.tick() / 100
            if self.gameRun and hasattr(self,"level") and self.level.gameStatus =="run":
                self.level.run(dt)
            elif hasattr(self,"level") and self.level.gameStatus !="run" and (not self.showMenu):
                score = self.level.player.score
                self.menu.display(self.level.gameStatus,score)
                self.level.bgm.stop()
                self.showMenu = True
                self.__delattr__('level')
                self.gameRun = False
            elif not self.showMenu:
                self.menu.display("start",0)
                self.showMenu = True
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    menu = Menu()
    game = Game()
    game.run()
