from datetime import datetime
import urllib2
import json
import re
import time

from module import Module
import render


class WeatherModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self.zip_code = context.config.get("Informant", "zip_code")
        if len(self.zip_code) == 0:
            self.zip_code = self._get_geoip()
        self.api_key = context.config.get("Informant", "api_key")
        self.temp_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.weather_label = render.OutlinedTextImg(color="#ffffff", outlinesize=2, size=60)
        self.updated_label = render.TextImg(color="#ffffff", size=20)
        self.sun_label = render.TextImg(color="#ffffff", size=20)
        self.img = None
        self.temp_f = ""
        self._i = 0
        self._updated_time = None

    @staticmethod
    def _get_geoip():
        try:
            response = urllib2.urlopen('http://www.geoiptool.com/en/').read()
            matchs = re.search(r"class=\"arial_bold\">(\d{5})</td>", response)
            return matchs.group(1)
        except:
            return "98052"

    @staticmethod
    def _kelvin_to_fahrenheit(degees_kelvin):
        return int(round((int(degees_kelvin) * 9 / 5.0) - 459.67))

    @staticmethod
    def _format_time(t):
        hour = str(int(time.strftime("%I", t)))
        rest = time.strftime(":%M%p", t).lower()
        return hour + rest

    def update_interval(self):
        return 30 * 60

    def update(self, context):
        try:
            self._i = 0
            url = "http://api.openweathermap.org/data/2.5/weather?q=%s" % self.zip_code
            result = json.load(urllib2.urlopen(url, timeout=120))
            self.temp_f = "%d %sF" % (self._kelvin_to_fahrenheit(result['main']['temp']), u'\N{DEGREE SIGN}')
            self.weather_label.set_text(result['weather'][0]['main'])
            sunrise = self._format_time(time.localtime(int(result['sys']['sunrise'])))
            sunset = self._format_time(time.localtime(int(result['sys']['sunset'])))
            self.sun_label.set_text("Sun: %s - %s" % (sunrise, sunset))
            self._updated_time = time.time()
        except Exception as e:
            self.temp_f = "Error: %s" % e

    def render(self, screen, context):
        # temperature
        self.temp_label.render(screen, 50, context.height - 150, self.temp_f)
        # temperature string
        self.weather_label.render(screen, 450, context.height - 150)
        # updated
        if self._updated_time is not None:
            self.updated_label.render(screen, 50, context.height - 50,
                                      "Updated " + str(int((time.time() - self._updated_time) / 60)) + " min ago")
        self.sun_label.render(screen, 300, context.height - 50)

