import urllib
import json

import render
import pygame


class Module():
    def __init__(self):
        pass

    def render(self, screen):
        pass


class WeatherModule(Module):
    def __init__(self):
        Module.__init__(self)
        self.label = render.TextImg(color="blue")
        self.img = None
        self.temp_f = 999
        self._i = 0
        self.get_weather()


    def get_weather(self):
        try:
            self._i = 0
            url = 'http://api.wunderground.com/api/c5cec5a481c71293/conditions/q/98052.json'
            result = json.load(urllib.urlopen(url))
            self.temp_f = result['current_observation']['temp_f']
            icon = result['current_observation']['weather']
            self.img = pygame.image.load("media/weather/" + icon + ".gif").convert()
            pass
        except Exception:


        def render(self, screen):
            self._i += 1
            if self._i > 60:
                self.get_weather()
            self.label.render(screen, 500, 500, "%.1f F" % self.temp_f)
            if self.img is not None:
                screen.blit(self.img, (100, 100))
