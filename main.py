import sys
import pygame as pg
import constants as c
from column import Column
import sorting

pg.init()
main_clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_W,c.SCREEN_H))
cols = Column.get_uniform_cols(c.SCREEN_W // c.COL_W)
gen = sorting.bubblesort_gen(cols)

while True:
    screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                cols = Column.get_uniform_cols(c.SCREEN_W // c.COL_W)
                gen = sorting.bubblesort_gen(cols)
    try:
        cols = next(gen)
    except StopIteration:
        pass

    for col in cols:
        col.draw(screen)
    pg.display.update()
    # print(cols)
    main_clock.tick(60)