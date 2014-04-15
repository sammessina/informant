import urllib
import json
import os
import StringIO

import render
from render import Module
import pygame


class BingBGModule(Module):
    def __init__(self):
        Module.__init__(self)
        self._i = 0
        self.img = None
        self.img_url = None
        self.img_rect = None
        self.get_bg()

    def get_bg(self):
        try:
            self._i = 0
            url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
            result = json.load(urllib.urlopen(url))
            self.img_url = "http://www.bing.com%s" % result['images'][0]['url']
            f = StringIO.StringIO(urllib.urlopen(self.img_url).read())
            self.img = pygame.image.load(f, self.img_url).convert()
            self.img_rect = self.img.get_rect()
        except Exception as e:
            pass

    def render(self, screen, screen_info):
        self._i += 1
        # Grab image once every 8 hours
        if self._i > 8 * 60 * 120:
            self.get_bg()
        if self.img is not None:
            screen.blit(self.img, (
            int((screen_info.width - self.img_rect.width) / 2), int((screen_info.height - self.img_rect.height) / 2)))
