import pygame as pg
from pygame.locals import *
from sys import exit
pg.init()

screen = pg.display.set_mode((640, 480))

while 1:
    for event in pg.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
    pg.display.update()