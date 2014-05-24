import calendar
import urllib2
import json
import httplib
import time
import os

import render
#import render.Module as Module
import render
import pygame


class NetworkModule(render.Module):
    def __init__(self, screen_info):
        render.Module.__init__(self, screen_info)
        self.label = render.OutlinedTextImg(color="red", outlinesize=2, size=60)
        self._i = 0
        self._net_error = False
        self._api_error = False
        self._offset = 0
        self.get_time()

    def get_time(self):
        try:
            self._net_error = False
            self._api_error = False
            self._i = 0
            url = 'http://www.timeapi.org/utc/now'
            response = urllib2.urlopen(url, timeout=120).read()
            result = time.strptime(response, "%Y-%m-%dT%H:%M:%S+00:00")
            self._offset = calendar.timegm(time.gmtime()) - calendar.timegm(result)
        except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException) as e:
            # network problem
            self._net_error = True
            pass
        except Exception as e:
            # error parsing data
            self._api_error = True

    def render(self, screen, screen_info):
        self._i += 1
        if self._i > 180 * 30:
            self.get_time()
        if abs(self._offset) > 60:
            self.label.render(screen, screen_info.width - 450, screen_info.height - 550, "Time Incorrect")
