import sys
import random
from time import strftime, localtime

import pygame
from pygame.locals import *

from render import TextImg, MultiColoredTextImg
from modules import weather



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
fps_target = 30

fpsLabel = TextImg(color="red")

loadedModules = [weather.WeatherModule()]

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
    thetime = localtime()  # place i in parens for test mode
    minute = strftime("%M", thetime)
    clock.set_text(0, str(int(strftime("%I", thetime))))
    clock.set_text(2, minute)

    clock.render(screen, time_x, time_y)
    # todo ugly bug: first frame will be at wrong coord
    if minute != last_minute:
        last_minute = minute
        time_x = random.randrange(max(1, screen_w - clock.width))
        time_y = random.randrange(max(1, screen_h - clock.height))

    for module in loadedModules:
        module.render(screen)

    fps = int(fpsClock.get_fps())
    if fps < .85 * fps_target:
        fpsLabel.render(screen, 0, 0, str(fps) + " FPS")
    pygame.display.update()
    fpsClock.tick(fps_target)