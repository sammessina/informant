import pygame
from pygame.locals import Color

__author__ = 'Sam'

#todo: port to https://github.com/tipam/pi3d

class TextRendererBase():
    def __init__(self):
        self._image = None
        self._rect = None

    def _render(self):
        self._rect = self._image.get_rect()

    def render(self, screen, x, y, text=None):
        pass

    def render_width(self):
        if self._image is None:
            self._render()
        return self._rect.width

    def render_height(self):
        if self._image is None:
            self._render()
        return self._rect.height


class TextImg(TextRendererBase):
    def __init__(self, font=None, color="white", size=32):
        TextRendererBase.__init__(self)
        self._color = Color(color)
        self._text = None
        self._font = font if font is not None else pygame.font.Font(pygame.font.match_font('Arial'), size)

    def _render(self):
        self._image = self._font.render(self._text, True, self._color)
        self._rect = self._image.get_rect()

    def set_text(self, text):
        if text != self._text:
            self._text = str(text)
            self._image = None

    def get_text(self):
        return self._text

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


class MultiColoredTextImg():
    def __init__(self, font=None, colors=(), parts=None):
        self.width = 0
        self.height = 0
        if parts is not None:
            self._parts = parts
        else:
            self._parts = []
            for color in colors:
                self._parts.append(TextImg(font, color))

    def set_text(self, index, text):
        self._parts[index].set_text(text)

        offset = 0
        for part in self._parts:
            offset += part.render_width()
            self.height = part.render_height()
        self.width = offset

    def render(self, screen, x, y):
        offset = 0
        for part in self._parts:
            part.render(screen, x + offset, y)
            offset += part.render_width()


class OutlinedTextImg(TextRendererBase):
    def __init__(self, font=None, color="white", size=32, outercolor="black", outlinesize=1):
        TextRendererBase.__init__(self)
        self._outlinesize = outlinesize
        self._inner_text = TextImg(font, color, size)
        self._outer_text = TextImg(font, outercolor, size)

    def _render(self):
        self._image = pygame.Surface((self._inner_text.render_width() + 2 * self._outlinesize,
                                      self._inner_text.render_height() + 2 * self._outlinesize), pygame.SRCALPHA)
        self._image.set_alpha(0)
        for x in range(0, 2 + 1):
            for y in range(0, 2 + 1):
                if not (x == 1 and y == 1):
                    self._outer_text.render(self._image, x * self._outlinesize, y * self._outlinesize)
        self._inner_text.render(self._image, self._outlinesize, self._outlinesize)
        self._rect = self._image.get_rect()

    def set_text(self, text):
        if self._inner_text.get_text() == text:
            return
        self._image = None
        self._inner_text.set_text(text)
        self._outer_text.set_text(text)

    def render(self, screen, x, y, text=None):
        if text is not None:
            self.set_text(text)
        if self._image is None:
            self._render()
        self._rect.topleft = (x, y)
        screen.blit(self._image, self._rect)


class Gradient():
    def __init__(self, width, height, topcolor, bottomcolor):
        self._image = pygame.Surface((width, height), pygame.SRCALPHA)
        self._image.set_alpha(0)
        self._rect = self._image.get_rect()
        color = pygame.Color("black")
        for y in range(0, height):
            scale = y / float(height)
            color.r = int((topcolor.r * (1 - scale)) + (bottomcolor.r * scale))
            color.g = int((topcolor.g * (1 - scale)) + (bottomcolor.g * scale))
            color.b = int((topcolor.b * (1 - scale)) + (bottomcolor.b * scale))
            color.a = int((topcolor.a * (1 - scale)) + (bottomcolor.a * scale))
            pygame.draw.line(self._image, color, (0, y), (width - 1, y))

    def render(self, screen, x, y):
        self._rect.topleft = (x, y)
        screen.blit(self._image, self._rect)


class ScreenInfo():
    def __init__(self):
        self.width = 0
        self.height = 0


class Module():
    def __init__(self):
        pass

    def render(self, screen, screen_info):
        pass

