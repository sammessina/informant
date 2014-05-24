from argparse import _ActionsContainer
import sys
import random
import time
from time import strftime, localtime

import pygame
from pygame.locals import *

from render import TextImg, MultiColoredTextImg, ScreenInfo, OutlinedTextImg
from modules import weather, bingbg, network, clock


class Informant():
    FPS_TARGET = 2

    def __init__(self):
        self.screen = None
        self.screen_info = ScreenInfo()

    def displayLoadingScreen(self):
        self.screen.fill(Color("black"))
        label = TextImg(size=80, color="#222222")
        label.set_text("loading")
        label.render(self.screen, (self.screen_info.width - label.render_width()) / 2,
                     (self.screen_info.height - label.render_height()) / 2)
        pygame.display.update()

    def main(self):
        pygame.init()
        fps_clock = pygame.time.Clock()
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
        #pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('informant')

        self.screen = pygame.display.get_surface()
        self.screen_info.width = pygame.display.Info().current_w
        self.screen_info.height = pygame.display.Info().current_h

        fps_label = TextImg(color="red")

        self.displayLoadingScreen()

        loaded_modules = [
            bingbg.BingBGModule(self.screen_info),
        #    weather.WeatherModule(self.screen_info),
            network.NetworkModule(self.screen_info),
            clock.ClockModule(self.screen_info)
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill(Color("black"))

            for module in loaded_modules:
                module.render(self.screen, self.screen_info)

            fps = float(fps_clock.get_fps())
            if fps < int(.85 * self.FPS_TARGET):
                fps_label.render(self.screen, 0, 0, "%.1f FPS" % fps)
            pygame.display.update()
            fps_clock.tick(self.FPS_TARGET)