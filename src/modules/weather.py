import urllib2
import json
import os
import time
import informant
import render
import pygame


class WeatherModule(render.Module):
    def __init__(self, context):
        render.Module.__init__(self, context)
        self.zip_code = context.config.get("Informant", "zip_code")
        if len(self.zip_code) == 0:
            self.bluetooth_address = "98052"
        self.temp_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.weather_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.updated_label = render.TextImg(color="#ffffff", size=20)
        self.img = None
        self.temp_f = 999
        self._i = 0
        self._updated_time = None
        self.get_weather()

    def get_weather(self):
        try:
            self._i = 0
            url = 'http://api.wunderground.com/api/c5cec5a481c71293/conditions/q/' + self.zip_code + '.json'
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
        self._i += 1
        if self._i > 30 * (60 * informant.Informant.FPS_TARGET):
            self.get_weather()

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

