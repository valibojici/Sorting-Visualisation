import sys
import pygame as pg
import constants as c
import column as col

pg.init()

screen = pg.display.set_mode((c.SCREEN_W,c.SCREEN_H))
cols = col.Column.get_uniform_cols(c.SCREEN_W // c.COL_W)


while True:
    screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    for col in cols:
        col.draw(screen)
    pg.display.update()
    