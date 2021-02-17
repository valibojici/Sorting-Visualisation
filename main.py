import sys
import pygame as pg
import constants as c
from column import Column
import sorting
from slider import Slider

pg.init()
main_clock = pg.time.Clock()

def update_cols_and_draw(surface,collumns,generator):
    if collumns is not None:
        for idx,collumn in enumerate(collumns):
            collumn.draw(surface,idx)
        try:
            collumns = next(generator)
        except StopIteration:
            pass

def triangle_collide_point(t_coords,p_coords):
    # point is inside the triangle if area
    # of triangle is the sum of areas of triangles
    def area(p1,p2,p3):
        x1,y1 = p1
        x2,y2 = p2
        x3,y3 = p3
        return abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2
    t_area = area(t_coords[0],t_coords[1],t_coords[2])
    area1 = area(t_coords[0],t_coords[1],p_coords)
    area2 = area(t_coords[1],t_coords[2],p_coords)
    area3 = area(t_coords[0],t_coords[2],p_coords)
    return abs(t_area - (area1 + area2 + area3)) < 300


def menu():
    screen = pg.display.set_mode((c.SCREEN_W,c.SCREEN_H))
    # list of collumns
    cols = None
    # generator for sorting states
    gen = None

    sort_gen_idx = 0
    click = False
    click_down = False
    
    # speed slider
    speed_slider = Slider(400,170, 400, 30, min_val=0, max_val=200,start=c.FPS,step=5)
    # number of elements slider
    # elem_slider = Slider(400,320,400,30,min_val=5,max_val=300,start=c.COL_NO,step=5)
    elem_slider = Slider(400,320,400,30,values=[x for x in range(4,601) if c.SCREEN_W % x == 0])
    while True:
        screen.fill((0,0,0))


        click = False
        # print(c.FPS,circle_center)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                click = True
                click_down = True
            elif event.type == pg.MOUSEBUTTONUP:
                click_down = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    cols = Column.get_uniform_cols(c.COL_NO)
                    gen = sorting.sort_gen[sort_gen_idx](cols,0,len(cols)-1)
                    visualize(screen,cols,gen,sort_gen_idx)
        # draw left triangle
        left_triangle = [(400,20),(400,50),(375,35)]
        pg.draw.polygon(screen,(255,255,255),left_triangle)
        # draw right triangle
        right_triangle = [(800,20),(800,50),(825,35)]
        pg.draw.polygon(screen,(255,255,255),right_triangle)
        
        # check for triangle click and update sort_gen_idx
        if click and triangle_collide_point(left_triangle,pg.mouse.get_pos()):
            sort_gen_idx = sort_gen_idx - 1 if sort_gen_idx > 0 else len(c.SORT_TEXT) - 1
        elif click and triangle_collide_point(right_triangle,pg.mouse.get_pos()):
            sort_gen_idx = sort_gen_idx + 1 if sort_gen_idx < len(c.SORT_TEXT) - 1 else 0
        
        # get "sorting" text
        text = c.SORT_TEXT[sort_gen_idx]
        text_w = text.get_size()[0]
        # blit "sorting" text to screen
        screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 20))
        
        # get "speed" text
        text = c.SPEED_TEXT
        #blit "speed" text to screen
        text_w = text.get_size()[0]
        screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 100))

        # get speed value text
        text = c.GET_TEXT(str(max(1,speed_slider.get_value()))+" FPS")
        # blit speed value text to screen
        text_h = text.get_size()[1]
        screen.blit(text,(830,speed_slider.center[1] - text_h / 2))

        # get "number of elements text"
        text = c.NUMBER_TEXT
        #blit "speed" text to screen
        text_w = text.get_size()[0]
        screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 250))

        # get number of elements value text
        text = c.GET_TEXT(elem_slider.get_value())
        # blit number of elements value text to screen
        text_h = text.get_size()[1]
        screen.blit(text,(830,elem_slider.center[1] - text_h / 2))

        # # get "compare" text
        # text = c.COMPARE_TEXT
        # # blit "compare" text to screen
        # text_w = text.get_size()[0]
        # screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 400))

        # # get "instructions" text
        textList = c.INSTRUC_TEXT
        for offset,text in enumerate(textList):
            text_w = text.get_size()[0]
            screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 380 + 40 * offset))

        # draw speed slider and check for updates to slider
        speed_slider.draw(screen)
        if click_down:
            speed_slider.update_mouse(pg.mouse.get_pos())
            c.FPS = max(1,speed_slider.get_value())

        # draw number of elements slider and check for updates
        elem_slider.draw(screen)
        if click_down:
            elem_slider.update_mouse(pg.mouse.get_pos())
            c.COL_NO = elem_slider.get_value()
            c.COL_W = c.SCREEN_W // c.COL_NO

        
        pg.display.flip()
        main_clock.tick(60)

def visualize(screen,cols,gen,idx_sort):
    while True:
        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cols = Column.get_uniform_cols(c.COL_NO)
                    gen = sorting.sort_gen[idx_sort](cols,0,c.COL_NO-1)
                if event.button == 4: 
                    if c.FPS == 0: c.FPS = 1
                    else: c.FPS = min(c.FPS * 2, 200)
                if event.button == 5: 
                    c.FPS = c.FPS // 2
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
        if c.FPS == 0: continue
        update_cols_and_draw(screen,cols,gen)
        pg.display.flip()
        
        main_clock.tick(c.FPS) 

menu()