import urllib
import json
import os

import render
#import render.Module as Module
from render import Module
import pygame


class WeatherModule(Module):
    GRADIENT_SIZE = 300
    def __init__(self):
        Module.__init__(self)
        self.temp_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.weather_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=50)
        self.img = None
        self.temp_f = 999
        self._i = 0
        self._gradient = None
        self.get_weather()

    def get_weather(self):
        try:
            self._i = 0
            url = 'http://api.wunderground.com/api/c5cec5a481c71293/conditions/q/98052.json'
            result = json.load(urllib.urlopen(url))
            self.temp_f = "%.1f F" % result['current_observation']['temp_f']
            #a/b/nt_clear.gif -> nt_clear
            icon = os.path.splitext(os.path.basename(result['current_observation']['icon_url']))[0]
            self.weather_label.set_text(result['current_observation']['weather'])
            self.img = pygame.image.load("media/weather/" + icon + ".gif").convert()
        except Exception as e:
            self.temp_f = "%s" % e

    def render(self, screen, screen_info):
        self._i += 1
        if self._i > 180 * 30:
            self.get_weather()
        if self._gradient is None:
            self._gradient = render.Gradient(screen_info.width, self.GRADIENT_SIZE, pygame.Color(0, 0, 0, 0), pygame.Color(255, 0, 0, 255))

        self._gradient.render(screen, 0, screen_info.height - self.GRADIENT_SIZE)
        self.temp_label.render(screen, screen_info.width - 500, screen_info.height - 150, self.temp_f)
        self.weather_label.render(screen, 500, screen_info.height - 150)
        if self.img is not None:
            screen.blit(self.img, (100, screen_info.height - 150))
