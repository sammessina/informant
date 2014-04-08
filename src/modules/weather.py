import urllib
import json

import render
import pygame


class Module():
    def __init__(self):
        pass

    def render(self, screen, screen_info):
        pass


class WeatherModule(Module):
    def __init__(self):
        Module.__init__(self)
        self.label = render.TextImg(color="blue", size=40)
        self.img = None
        self.temp_f = 999
        self._i = 0
        self.get_weather()

    def get_weather(self):
        try:
            self._i = 0
            url = 'http://api.wunderground.com/api/c5cec5a481c71293/conditions/q/98052.json'
            result = json.load(urllib.urlopen(url))
            self.temp_f = "%.1f F" % result['current_observation']['temp_f']
            icon = result['current_observation']['icon']
            self.img = pygame.image.load("media/weather/" + icon + ".gif").convert()
        except Exception as e:
            self.temp_f = "%s" % e

    def render(self, screen, screen_info):
        self._i += 1
        if self._i > 180 * 30:
            self.get_weather()
        self.label.render(screen, 500, screen_info.height - 150, self.temp_f)
        if self.img is not None:
            screen.blit(self.img, (100, screen_info.height - 150))
