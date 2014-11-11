from datetime import datetime
import urllib2
import json
import re
import time
import pygame

from module import Module
import render


class WeatherModule(Module):
    GRADIENT_SIZE = 300

    def __init__(self, context):
        Module.__init__(self, context)
        self._gradient = render.Gradient(context.width, self.GRADIENT_SIZE, pygame.Color(0, 0, 0, 0),
                                         pygame.Color(0, 0, 0, 255))
        self.zip_code = context.get_config("zip_code")
        if len(self.zip_code) == 0:
            self.zip_code = self._get_geoip()
        self.api_key = context.get_config("api_key")
        self.temp_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.weather_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.updated_label = render.TextImg(color="#ffffff", size=20)
        self.sun_label = render.TextImg(color="#ffffff", size=20)
        self.temp_f = ""
        self._updated_time = None
        self._had_error = False

    @staticmethod
    def _get_geoip():
            return ""

    @staticmethod
    def _kelvin_to_fahrenheit(degees_kelvin):
        return int(round((int(degees_kelvin) * 9 / 5.0) - 459.67))

    @staticmethod
    def _format_time(t):
        hour = str(int(time.strftime("%I", t)))
        rest = time.strftime(":%M%p", t).lower()
        return hour + rest

    def update_interval(self):
        if self._had_error:
            return 5 * 60
        return 30 * 60

    def update(self, context):
        try:
            url = "http://api.openweathermap.org/data/2.5/weather?q=%s" % self.zip_code
            result = json.load(urllib2.urlopen(url, timeout=120))
            self.temp_f = "%d %sF" % (self._kelvin_to_fahrenheit(result['main']['temp']), u'\N{DEGREE SIGN}')
            self.weather_label.set_text(result['weather'][0]['main'])
            sunrise = self._format_time(time.localtime(int(result['sys']['sunrise'])))
            sunset = self._format_time(time.localtime(int(result['sys']['sunset'])))
            self.sun_label.set_text("Sunlight: %s - %s" % (sunrise, sunset))
            self._updated_time = time.time()
            self._had_error = False
        except:
            self._had_error = True

    def render(self, screen, context):
        self._gradient.render(screen, 0, context.height - self.GRADIENT_SIZE)
        # temperature
        self.temp_label.render(screen, 50, context.height - 150, self.temp_f)
        # temperature string
        self.weather_label.render(screen, 450, context.height - 150)
        # updated
        if self._updated_time is not None:
            self.updated_label.render(screen, 50, context.height - 50,
                                      "Updated " + str(int((time.time() - self._updated_time) / 60)) + " min ago")
        self.sun_label.render(screen, 300, context.height - 50)

