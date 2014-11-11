import urllib2
import render
from module import Module


class PlantModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self._plantserver = context.get_config("plant_server")
        self._red_label = render.OutlinedTextImg(color="red", outlinesize=2, size=60)
        self._had_error = False
        self._status = ""

    def update_interval(self):
        if len(self._plantserver) == 0:
            return 60 * 60

        if self._had_error:
            return 60  # retry every minute

        return 15 * 60  # refresh every 15 minutes

    def update(self, context):
        if len(self._plantserver) == 0:
            return
        url = "http://%s" % self._plantserver
        for i in xrange(1, 3):
            try:
                self._status = urllib2.urlopen(url, timeout=120).read()
                self._had_error = False
                return
            except:
                pass
        self._had_error = True

    def render(self, screen, context):
        if len(self._plantserver) == 0:
            return

        # normal condition
        if not self._had_error and self._status == "wet":
            return

        label = "Water plant!" if not self._had_error else "Error fetching plant status"

        self._red_label.render(screen, 50, context.height - 150 - 80, label)