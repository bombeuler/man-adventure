import pygame, sys
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
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill("black")
            dt = self.clock.tick() / 100
            self.level.run(dt)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
