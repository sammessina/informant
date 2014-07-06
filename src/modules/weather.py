import urllib2
import json
import os
import time

import pygame

import informant
from module import Module
import render


class WeatherModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self.zip_code = context.config.get("Informant", "zip_code")
        if len(self.zip_code) == 0:
            self.zip_code = "98052"
        self.api_key = context.config.get("Informant", "api_key")
        self.temp_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.weather_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.updated_label = render.TextImg(color="#ffffff", size=20)
        self.img = None
        self.temp_f = ""
        self._i = 0
        self._updated_time = None

    def update_interval(self):
        return 30 * 60

    def update(self, context):
        try:
            self._i = 0
            url = "http://api.wunderground.com/api/%s/conditions/q/%s.json" % (self.api_key, self.zip_code)
            result = json.load(urllib2.urlopen(url, timeout=120))
            self.temp_f = "%.1f F" % result['current_observation']['temp_f']
            # "a/b/nt_clear.gif" -> "nt_clear"
            icon = os.path.splitext(os.path.basename(result['current_observation']['icon_url']))[0]
            self.weather_label.set_text(result['current_observation']['weather'])
            self._updated_time = time.time()
            self.img = pygame.image.load("media/weather/" + icon + ".gif").convert()
        except Exception as e:
            self.temp_f = "%s" % e

    def render(self, screen, context):
        # temperature
        self.temp_label.render(screen, 50, context.height - 150, self.temp_f)
        # icon
        if self.img is not None:
            screen.blit(self.img, (300, context.height - 150))
        # temperature string
        self.weather_label.render(screen, 450, context.height - 150)
        if self._updated_time is not None:
            self.updated_label.render(screen, 50, context.height - 50,
                                      "Updated " + str(int((time.time() - self._updated_time) / 60)) + " min ago")

