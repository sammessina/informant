import pygame
import sys
import random
from pygame.locals import *
from time import strftime, localtime


class TextImg():
    def __init__(self, font=None, color="white"):
        self._color = Color(color)
        self._text = ""
        self._font = font if font is not None else pygame.font.Font(pygame.font.match_font('Arial'), 100)
        self._image = None
        self._rect = None

    def _render(self):
        self._image = self._font.render(self._text, True, self._color)
        self._rect = self._image.get_rect()

    def set_text(self, text):
        if text != self._text:
            self._text = text
            self._image = None

    def render(self, screen, x, y, text=None):
        if self._image is None:
            self._render()
        self._rect.topleft = (x, y)
        screen.blit(self._image, self._rect)

    def render_width(self):
        return self._rect.width

    def render_height(self):
        return self._rect.height


class MultiColoredTextImg():
    def __init__(self, font=None, colors=()):
        self._parts = []
        self.width = 0
        self.height = 0
        for color in colors:
            self._parts.append(TextImg(font, color))

    def set_text(self, index, text):
        self._parts[index].set_text(text)

    def render(self, screen, x, y):
        offset = 0
        for part in self._parts:
            part.render(screen, x + offset, y)
            offset += part.render_width()
            self.height = part.render_height()
        self.width = offset


pygame.init()
fpsClock = pygame.time.Clock()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)
#pygame.display.set_mode((1024, 600), pygame.RESIZABLE | pygame.HWSURFACE)
pygame.mouse.set_visible(False)
pygame.display.set_caption('Clock')

clock = MultiColoredTextImg(pygame.font.Font("NixieOne-Regular.otf", 500), ("white", "gray", "white"))
clock.set_text(1, ":")

random.seed()

i = 0
screen = pygame.display.get_surface()
screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h
time_x = 0
time_y = 0
last_minute = -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    screen.fill(Color("black"))

    i += 10
    thetime = localtime() # place i in parens for test mode
    minute = strftime("%M", thetime)
    clock.set_text(0, str(int(strftime("%I", thetime))))
    clock.set_text(2, minute)

    clock.render(screen, time_x, time_y)
    # todo ugly bug: first frame will be at wrong coord
    if minute != last_minute:
        last_minute = minute
        time_x = random.randrange(screen_w - clock.width)
        time_y = random.randrange(screen_h - clock.height)

    pygame.display.update()
    fpsClock.tick(30)