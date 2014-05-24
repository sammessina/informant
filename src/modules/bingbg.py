import urllib2
import json
import os
import StringIO

import pygame
import render


class BingBGModule(render.Module):
    GRADIENT_SIZE = 300

    def __init__(self, screen_info):
        render.Module.__init__(self, screen_info)
        self._i = -2
        self.img = None
        self.img_url = None
        self.img_rect = None
        self._gradient = render.Gradient(screen_info.width, self.GRADIENT_SIZE, pygame.Color(0, 0, 0, 0),
                                         pygame.Color(0, 0, 0, 255))

    def get_bg(self, screen_info):
        resolutions = ["1920x1080", "1920x1200", "1366x768"]
        try:
            self._i = 0
            url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
            result = json.load(urllib2.urlopen(url, timeout=120))
            self.img_url = "http://www.bing.com%s" % result['images'][0]['url']
            f = ''
            for resolution in resolutions:
                new_url = self.img_url.replace("1366x768", resolution, 1)
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
            scale = (1.0 * screen_info.height / img_raw.get_rect().height)
            new_width = int(img_raw.get_rect().width * scale)
            new_height = int(img_raw.get_rect().height * scale)
            img_raw = pygame.transform.smoothscale(img_raw, (new_width, new_height))
            self.img = img_raw
            self.img_rect = self.img.get_rect()
        except:
            pass

    def render(self, screen, screen_info):
        self._i += 1
        # Grab image once every 8 hours
        if self._i == -1 or self._i > 8 * 60 * 120:
            self.get_bg(screen_info)
        if self.img is not None:
            screen.blit(self.img,
                        (int((screen_info.width - self.img_rect.width) / 2),
                         int((screen_info.height - self.img_rect.height) / 2)))
            self._gradient.render(screen, 0, screen_info.height - self.GRADIENT_SIZE)
