import sys
import ConfigParser
import threading
import time
import os.path

import pygame
from pygame.locals import *

import render
from modules import weather, bingbg, clock, btscan, network


class Informant():
    FPS_TARGET = 2

    def __init__(self):
        self.screen = None
        self.context = InformantContext()
        self.modules = []

    def display_loading_screen(self):
        self.screen.fill(Color("black"))
        label = render.OutlinedTextImg(size=80, color="#222222", outercolor="white")
        label.set_text("loading")
        label.render(self.screen, (self.context.width - label.render_width()) / 2,
                     (self.context.height - label.render_height()) / 2)
        pygame.display.update()

    def read_config(self):
        config = ConfigParser.ConfigParser()
        config_paths = ["informant.override.ini", "/boot/informant.ini", "informant.ini", "../informant.ini"]
        for path in config_paths:
            if os.path.isfile(path):
                config.read(path)
                break
        self.context._config = config

    def update_screen_size(self, w, h):
        self.context.width = w
        self.context.height = h

    def main(self):
        self.read_config()
        pygame.init()
        fps_clock = pygame.time.Clock()
        if self.context.get_config("fullscreen") == "No":
            pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('informant')

        self.screen = pygame.display.get_surface()
        self.update_screen_size(pygame.display.Info().current_w, pygame.display.Info().current_h)

        fps_label = render.TextImg(color="red")

        self.display_loading_screen()

        loaded_modules = [
            bingbg.BingBGModule(self.context),
            weather.WeatherModule(self.context),
            btscan.BluetoothModule(self.context),
            network.NetworkModule(self.context),
            clock.ClockModule(self.context)
        ]

        for module in loaded_modules:
            mod = _ModuleRef()
            mod.module = module
            t = threading.Thread(target=mod.update_module, args=(self.context,))
            t.daemon = True
            t.start()
            mod.thread = t
            self.modules.append(mod)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.update_screen_size(event.w, event.h)

            self.screen.fill(Color("black"))

            for module in self.modules:
                module.module.render(self.screen, self.context)

            for i in range(len(self.modules)):
                module = self.modules[i]
                if not module.is_responding():
                    module.render_error(i, self.screen, self.context)

            fps = float(fps_clock.get_fps())
            if fps < int(.85 * self.FPS_TARGET) - .5:
                fps_label.render(self.screen, 0, 0, "%.1f FPS" % fps)
            pygame.display.update()
            fps_clock.tick(self.FPS_TARGET)


class InformantContext():
    def __init__(self):
        self.width = 0
        self.height = 0
        self._config = None

    def get_config(self, option):
        try:
            return self._config.get("Informant", option)
        except:
            return ""


class _ModuleRef():
    def __init__(self):
        self.module = None
        self.thread = None
        self._last_response = 0
        self._error_label = self.updated_label = render.OutlinedTextImg(color="#ff0000", size=30, outercolor="black")
        pass

    def update_module(self, context):
        while True:
            update_start = time.time()
            self.module.update(context)
            self._last_response = time.time() - update_start
            time.sleep(self.module.update_interval())

    # a module is marked as 'not responding' when it takes more than 5 minutes to update
    def is_responding(self):
        return self._last_response < 5 * 60

    def render_error(self, i, screen, context):
        self.updated_label.render(screen, 50, 50 + 50 * i,
                                  "Module %s is not responding" % self.module.__class__.__name__)