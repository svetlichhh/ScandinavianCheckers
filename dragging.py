import pygame as pg
from pygame.locals import *
from sys import exit
pg.init()

screen = pg.display.set_mode((640,480))

white = (255, 255, 255)
black = (0, 0, 0)

sprite_image = "shooter_dali.png"
sprite_surf = pg.image.load(sprite_image).convert_alpha()

sprite_rect = sprite_surf.get_rect()
spos = sprite_rect.topleft
screen.blit(sprite_surf, spos)

sprite_size = sprite_surf.get_size()

while 1:

    mpos = pg.mouse.get_pos()

    for event in pg.event.get():
        if pg.mouse.get_pressed()[0]:
            if spos[0] + sprite_size[0] >= mpos[0] >= spos[0] and spos[1] + sprite_size[1] >= mpos[1] >= spos[1]:
                mpos_dif = (pg.mouse.get_pos()[0] - mpos[0], pg.mouse.get_pos()[1] - mpos[1])

                spos = (spos[0] + mpos_dif[0], spos[1] + mpos_dif[1])
                   
                screen.fill(black)
                screen.blit(sprite_surf, spos)

        elif event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()

    pg.display.update()