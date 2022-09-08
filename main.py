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
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.gameRun = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_m:
                        self.gameRun = True
                        self.level = Level()
                        print("11")
            self.screen.fill("black")
            dt = self.clock.tick() / 100
            if self.gameRun:
                self.level.run(dt)
            else:
                self.menu.display("win",34)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    menu = Menu()
    game = Game()
    game.run()
