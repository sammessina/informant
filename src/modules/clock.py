import random
import datetime
import time
import pygame
import render


class ClockModule(render.Module):
    BOTTOM_PANEL_HEIGHT_PX = 300

    def __init__(self, context):
        render.Module.__init__(self, context)
        self.clockfont = pygame.font.Font("NixieOne-Regular.otf", int(context.height * .65))
        outline = pygame.Color(0)
        self.clock = render.MultiColoredTextImg(parts=[
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, outlinesize=2),
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, color="gray", outlinesize=2),
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, outlinesize=2)
        ])
        self.date_label = render.OutlinedTextImg(color="#ffffff", size=60)
        self.clock.set_text(1, ":")
        self._i = 0
        self.time_x = 0
        self.time_y = 0
        self.last_minute = -1
        random.seed()

    def wacky_colors(self):
        color = pygame.Color(0)
        # documentation is wrong about H range. It says [0-360] but 360 causes an OverflowError.
        color.hsva = (random.randint(0, 359), 100, 100, 100)
        outline = pygame.Color(0)
        self.clock = render.MultiColoredTextImg(parts=[
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, color=color, outlinesize=2),
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, color="gray", outlinesize=2),
            render.OutlinedTextImg(font=self.clockfont, outercolor=outline, color=color, outlinesize=2)
        ])
        self.clock.set_text(1, ":")

    def render(self, screen, context):
        self._i += 10
        thetime = time.localtime()  # place self._i in parens for test mode
        minute = time.strftime("%M", thetime)

        # todo ugly bug: first frame will be at wrong coord
        # actually it's kind of nice when the time changes and .5 seconds later moves
        if minute != self.last_minute:
            self.wacky_colors()  # todo: do this only if specified in config
            self.clock.set_text(0, str(int(time.strftime("%I", thetime))))
            self.clock.set_text(2, minute)
            self.last_minute = minute
            self.time_x = random.randrange(max(1, context.width - self.clock.width))
            self.time_y = random.randrange(max(1, context.height - self.clock.height - self.BOTTOM_PANEL_HEIGHT_PX))

        self.clock.render(screen, self.time_x, self.time_y)
        date_str = datetime.datetime.now().strftime("%A, %B %d")
        self.date_label.set_text(date_str)
        self.date_label.render(screen, context.width - self.date_label.render_width() - 100, context.height - 150)
