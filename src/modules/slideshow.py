import StringIO
import os
import pygame
import random
from module import Module


class SlideshowModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self.img = None
        self._next_index = 0
        self.img_rect = None
        self._files = []
        slideshow_dir = context.get_config("slideshow_dir")
        for filename in os.listdir(slideshow_dir):
            full_path = os.path.join(slideshow_dir, filename)
            if os.path.isfile(full_path):
                self._files.append(full_path)
        random.shuffle(self._files)


    def _fetch_new_image(self, context):
        try:
            f = StringIO.StringIO(open(self._files[self._next_index], "rb").read())
            img_raw = pygame.image.load(f, self._files[self._next_index]).convert()
            scale = (1.0 * context.width / img_raw.get_rect().width)
            new_width = int(img_raw.get_rect().width * scale)
            new_height = int(img_raw.get_rect().height * scale)
            img_raw = pygame.transform.smoothscale(img_raw, (new_width, new_height))
            self.img = img_raw
            self.img_rect = self.img.get_rect()
        except:
            pass
        self._next_index = (self._next_index + 1) % len(self._files)

    # New image every 5 minutes
    def update_interval(self):
        return 5 * 60

    def update(self, context):
        if len(self._files) == 0:
            return
        self._fetch_new_image(context)

    def render(self, screen, context):
        if self.img is not None:
            screen.blit(self.img,
                        (int((context.width - self.img_rect.width) / 2),
                         int((context.height - self.img_rect.height) / 2)))
