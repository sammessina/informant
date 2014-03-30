from argparse import _ActionsContainer
import sys
import random
import time
from time import strftime, localtime

import pygame
from pygame.locals import *

from render import TextImg, MultiColoredTextImg
from modules import weather


class Informant():
    def __init__(self):
        self.screen = None

    def displayLoadingScreen(self):
        self.screen.fill(Color("black"))
        label = TextImg(size=80, color="#181818")
        label.set_text("informantboard")
        label.render(self.screen, (self.screen_w - label.render_width())/2, (self.screen_h - label.render_height())/2)
        pygame.display.update()

    def main(self):
        pygame.init()
        fpsClock = pygame.time.Clock()
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
        #pygame.display.set_mode((1024, 600), pygame.RESIZABLE | pygame.HWSURFACE)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Clock')

        clock = MultiColoredTextImg(pygame.font.Font("NixieOne-Regular.otf", 500), ("white", "gray", "white"))
        clock.set_text(1, ":")

        random.seed()

        i = 0
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        time_x = 0
        time_y = 0
        last_minute = -1
        fps_target = 10

        fpsLabel = TextImg(color="red")

        self.displayLoadingScreen()

        loadedModules = [weather.WeatherModule()]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if i % 500 == 0:
                self.screen.fill(Color("black"))

            i += 10
            thetime = localtime()  # place i in parens for test mode
            minute = strftime("%M", thetime)
            clock.set_text(0, str(int(strftime("%I", thetime))))
            clock.set_text(2, minute)

            clock.render(self.screen, time_x, time_y)
            # todo ugly bug: first frame will be at wrong coord
            if minute != last_minute:
                last_minute = minute
                time_x = random.randrange(max(1, self.screen_w - clock.width))
                time_y = random.randrange(max(1, self.screen_h - clock.height))

            for module in loadedModules:
                module.render(self.screen)

            fps = int(fpsClock.get_fps())
            if fps < .85 * fps_target:
                fpsLabel.render(self.screen, 0, 0, str(fps) + " FPS")
            pygame.display.update()
            fpsClock.tick(fps_target)