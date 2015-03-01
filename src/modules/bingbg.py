import urllib2
import json
import StringIO

import pygame
from module import Module
import render


class BingBGModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self.img = None
        self.img_url = None
        self.img_rect = None

    # Grab image once every 2 hours
    def update_interval(self):
        return 2 * 60 * 60

    def update(self, context):
        resolutions = ["1920x1080", "1920x1200", "1366x768"]
        try:
            url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
            result = json.load(urllib2.urlopen(url, timeout=120))
            self.img_url = "http://www.bing.com%s" % result['images'][0]['url']
            f = ''
            for resolution in resolutions:
                new_url = self.img_url.replace("1366x768", "%RES%", 1)
                new_url = new_url.replace("1920x1080", "%RES%", 1)
                new_url = new_url.replace("%RES%", resolution, 1)
                try:
                    f = StringIO.StringIO(urllib2.urlopen(new_url, timeout=120).read())
                    break
                except:
                    pass
            if f == '':
                return
            img_raw = pygame.image.load(f, self.img_url).convert()

            # resize image to fill screen
            # img_y/img_x = screen_y/screen_x
            # img_y = screen_y/screen_x*img_x
            # img_x =
            scale = (1.0 * context.height / img_raw.get_rect().height)
            new_width = int(img_raw.get_rect().width * scale)
            new_height = int(img_raw.get_rect().height * scale)
            img_raw = pygame.transform.smoothscale(img_raw, (new_width, new_height))
            self.img = img_raw
            self.img_rect = self.img.get_rect()
        except:
            pass

    def render(self, screen, context):
        if self.img is not None:
            screen.blit(self.img,
                        (int((context.width - self.img_rect.width) / 2),
                         int((context.height - self.img_rect.height) / 2)))
