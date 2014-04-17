import calendar
import urllib2
import json
import httplib
import time
import os

import render
#import render.Module as Module
from render import Module
import pygame


class NetworkModule(Module):
    def __init__(self):
        Module.__init__(self)
        self.label = render.OutlinedTextImg(color="red", outlinesize=2, size=60)
        self._i = 0
        self._error = False
        self._offset = 0
        self.get_time()

    def get_time(self):
        try:
            self._i = 0
            url = 'http://www.timeapi.org/utc/now'
            response = urllib2.urlopen(url).read()
            result = time.strptime(response, "%Y-%m-%dT%H:%M:%S+00:00")
            self._offset = calendar.timegm(time.gmtime()) - calendar.timegm(result)
            self._error = False
        except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException) as e:
            # network problem
            self._error = True
            pass
        except Exception as e:
            # error parsing data
            self._error = True

    def render(self, screen, screen_info):
        self._i += 1
        if self._i > 180 * 30:
            self.get_time()
        if self._error:
            self.label.render(screen, screen_info.width - 450, screen_info.height - 150, "Network Error")
        elif abs(self._offset) > 60:
            self.label.render(screen, screen_info.width - 450, screen_info.height - 150, "Time Offset")
