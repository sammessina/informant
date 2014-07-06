import calendar
import urllib2
import httplib
import time

from module import Module
import render


class NetworkModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self.label = render.OutlinedTextImg(color="red", outlinesize=2, size=60)
        self._net_error = False
        self._api_error = False
        self._offset = 0

    def update_interval(self):
        return 3 * 60

    def update(self, context):
        try:
            self._net_error = False
            self._api_error = False
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

    def render(self, screen, context):
        if abs(self._offset) > 60:
            self.label.render(screen, context.width - 450, context.height - 550, "Time Incorrect")
