import sys
import ConfigParser
import pygame
from pygame.locals import *

from render import TextImg, MultiColoredTextImg, InformantContext, OutlinedTextImg
from modules import weather, bingbg, network, clock, btscan


class Informant():
    FPS_TARGET = 2

    def __init__(self):
        self.screen = None
        self.context = InformantContext()

    def display_loading_screen(self):
        self.screen.fill(Color("black"))
        label = TextImg(size=80, color="#222222")
        label.set_text("loading")
        label.render(self.screen, (self.context.width - label.render_width()) / 2,
                     (self.context.height - label.render_height()) / 2)
        pygame.display.update()

    def read_config(self):
        config = ConfigParser.ConfigParser()
        config.read("/boot/informant.ini")
        self.context.config = config

    def main(self):
        pygame.init()
        fps_clock = pygame.time.Clock()
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
        #pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('informant')

        self.screen = pygame.display.get_surface()
        self.context.width = pygame.display.Info().current_w
        self.context.height = pygame.display.Info().current_h

        fps_label = TextImg(color="red")

        self.display_loading_screen()
        self.read_config()

        loaded_modules = [
            bingbg.BingBGModule(self.context),
            weather.WeatherModule(self.context),
            btscan.BluetoothModule(self.context),
            network.NetworkModule(self.context),
            clock.ClockModule(self.context)
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
                module.render(self.screen, self.context)

            fps = float(fps_clock.get_fps())
            if fps < int(.85 * self.FPS_TARGET) - .5:
                fps_label.render(self.screen, 0, 0, "%.1f FPS" % fps)
            pygame.display.update()
            fps_clock.tick(self.FPS_TARGET)