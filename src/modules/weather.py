import urllib
import json

import render


class Module():
    def __init__(self):
        pass

    def render(self, screen):
        pass


class WeatherModule(Module):
    def __init__(self):
        Module.__init__(self)
        url = 'http://api.wunderground.com/api/c5cec5a481c71293/conditions/q/98052.json'
        result = json.load(urllib.urlopen(url))
        self.temp_f = result['current_observation']['temp_f']
        self.label = render.TextImg(color="blue")

    def render(self, screen):
        self.label.render(screen, 500, 500, "%.1f F" % self.temp_f)
