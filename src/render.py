import pygame
from pygame.locals import Color

__author__ = 'Sam'


class TextImg():
    def __init__(self, font=None, color="white", size=32):
        self._color = Color(color)
        self._text = None
        self._font = font if font is not None else pygame.font.Font(pygame.font.match_font('Arial'), size)
        self._image = None
        self._rect = None

    def _render(self):
        self._image = self._font.render(self._text, True, self._color)
        self._rect = self._image.get_rect()

    def set_text(self, text):
        if text != self._text:
            self._text = str(text)
            self._image = None

    def set_color(self, color):
        self._color = Color(color)
        self._image = None

    def render(self, screen, x, y, text=None):
        if text is not None:
            self.set_text(text)
        if self._image is None:
            self._render()
        self._rect.topleft = (x, y)
        screen.blit(self._image, self._rect)

    def render_width(self):
        if self._image is None:
            self._render()
        return self._rect.width

    def render_height(self):
        if self._image is None:
            self._render()
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


class ScreenInfo():
    def __init__(self):
        self.width = 0
        self.height = 0


class Module():
    def __init__(self):
        pass

    def render(self, screen, screen_info):
        pass