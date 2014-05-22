from argparse import _ActionsContainer
import sys
import random
import time
from time import strftime, localtime

import pygame
from pygame.locals import *

from render import TextImg, MultiColoredTextImg, ScreenInfo, OutlinedTextImg
from modules import weather, bingbg, network


class Informant():
    BOTTOM_PANEL_HEIGHT_PX = 300
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
        fpsClock = pygame.time.Clock()
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
        #pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Clock')

        clockfont = pygame.font.Font("NixieOne-Regular.otf", 500)
        clock = MultiColoredTextImg(parts=[
            OutlinedTextImg(font=clockfont),
            OutlinedTextImg(font=clockfont, color="gray"),
            OutlinedTextImg(font=clockfont)
        ])
        clock.set_text(1, ":")

        random.seed()

        i = 0
        self.screen = pygame.display.get_surface()
        self.screen_info.width = pygame.display.Info().current_w
        self.screen_info.height = pygame.display.Info().current_h
        time_x = 0
        time_y = 0
        last_minute = -1

        fpsLabel = TextImg(color="red")

        self.displayLoadingScreen()

        loadedModules = [bingbg.BingBGModule(), weather.WeatherModule(), network.NetworkModule()]

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

            i += 10
            thetime = localtime()  # place i in parens for test mode
            minute = strftime("%M", thetime)
            clock.set_text(0, str(int(strftime("%I", thetime))))
            clock.set_text(2, minute)

            for module in loadedModules:
                module.render(self.screen, self.screen_info)

            clock.render(self.screen, time_x, time_y)
            # todo ugly bug: first frame will be at wrong coord
            if minute != last_minute:
                last_minute = minute
                time_x = random.randrange(max(1, self.screen_info.width - clock.width))
                time_y = random.randrange(max(1, self.screen_info.height - clock.height - self.BOTTOM_PANEL_HEIGHT_PX))

            fps = float(fpsClock.get_fps())
            if fps < int(.85 * self.FPS_TARGET):
                fpsLabel.render(self.screen, 0, 0, "%.1f FPS" % fps)
            pygame.display.update()
            fpsClock.tick(self.FPS_TARGET)