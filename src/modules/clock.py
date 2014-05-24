import calendar
import random
import urllib2
import json
import httplib
import time
import os

import pygame
from src import render


class ClockModule(render.Module):
    BOTTOM_PANEL_HEIGHT_PX = 300

    def __init__(self, screen_info):
        render.Module.__init__(self, screen_info)
        self.clockfont = pygame.font.Font("NixieOne-Regular.otf", int(screen_info.height * .6))
        outline = pygame.Color(0, 0, 0, 127)
        self.clock = render.MultiColoredTextImg(parts=[
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline),
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, color="gray"),
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline)
        ])
        self.clock.set_text(1, ":")
        self._i = 0
        self.time_x = 0
        self.time_y = 0
        self.last_minute = -1
        random.seed()

    def render(self, screen, screen_info):
        self._i += 10
        thetime = time.localtime()  # place self._i in parens for test mode
        minute = time.strftime("%M", thetime)
        self.clock.set_text(0, str(int(time.strftime("%I", thetime))))
        self.clock.set_text(2, minute)

        # todo ugly bug: first frame will be at wrong coord
        # actually it's kind of nice when the time changes and .5 seconds later moves
        if minute != self.last_minute:
            self.last_minute = minute
            self.time_x = random.randrange(max(1, screen_info.width - self.clock.width))
            self.time_y = random.randrange(
                max(1, screen_info.height - self.clock.height - self.BOTTOM_PANEL_HEIGHT_PX))

        self.clock.render(screen, self.time_x, self.time_y)
