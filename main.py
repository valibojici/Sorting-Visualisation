import sys
import pygame as pg
import constants as c
from column import Column
import sorting

pg.init()
main_clock = pg.time.Clock()
screen = pg.display.set_mode((c.SCREEN_W,c.SCREEN_H))

# list of collumns
cols = None
# generator for sorting states
gen = None


def update_cols_and_draw(collumns,generator,surface):
    if collumns is not None:
        try:
            collumns = next(generator)
        except StopIteration:
            pass
        for collumn in collumns:
            collumn.draw(surface)

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
    return abs(t_area - (area1 + area2 + area3)) < 1


class Slider:
    def __init__(self,left,top,width,height,min_val,max_val,default_value=0,increment=1):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.line_width = height / 8
        self.rect_bound = pg.Rect(left,top,width,height)
        self.center = self.rect_bound.center
        self.line = pg.Rect(left,top+self.height/2-self.line_width/2,width,self.line_width)
        self.circle_center = (default_value if default_value else left + width / 2, self.line.center[1])
    
    def draw(self,surface):
        pg.draw.rect(surface,(255,255,255),self.line)
        pg.draw.circle(surface,(255,255,255),self.circle_center,self.height / 2)

    def debug(self,surface):
        pg.draw.rect(surface,(255,255,255),self.rect_bound,1)

    def update_mouse(self,coords):
        if not self.rect_bound.collidepoint(pg.mouse.get_pos()):
            print('no collision')
            return
        print('collision')




def gui_draw():
    text_idx = 0
    click = False
    click_down = False
    
    # circle on line
    circle_center = (400 if c.FPS == 1 else c.FPS+400,0)


    # speed line

    x = Slider(400,400, 400, 30, 1, 400)

    while True:
        screen.fill((0,0,0))

        # x.debug(screen)
        x.draw(screen)

        click = False
        # print(c.FPS,circle_center)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                click = True
                click_down = True
            if event.type == pg.MOUSEBUTTONUP:
                click_down = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
        # draw left triangle
        left_triangle = [(400,20),(400,50),(375,35)]
        pg.draw.polygon(screen,(255,255,255),left_triangle)
        # draw right triangle
        right_triangle = [(800,20),(800,50),(825,35)]
        pg.draw.polygon(screen,(255,255,255),right_triangle)
        
        # check for triangle click and update text_idx
        if click and triangle_collide_point(left_triangle,pg.mouse.get_pos()):
            text_idx = text_idx - 1 if text_idx >= 0 else len(c.SORT_TEXT) - 1
        elif click and triangle_collide_point(right_triangle,pg.mouse.get_pos()):
            text_idx = text_idx + 1 if text_idx < len(c.SORT_TEXT) - 1 else 0
        
        # get sorting text
        text = c.SORT_TEXT[text_idx]
        text_w = text.get_size()[0]
        # blit sorting text to screen
        screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 20))
        
        #blit speed text to screen
        text = c.SPEED_TEXT
        text_w = text.get_size()[0]
        screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 100))

        line = pg.Rect(400,170,400,4)
        # rect containing line
        circle_rect = pg.Rect(400,170,420,40)
        circle_rect.center = line.center
        circle_center = (circle_center[0],line.center[1])

        # draw line
        pg.draw.rect(screen,(255,255,255),line)
        # draw speed value
        text = c.GET_TEXT(max(1,circle_center[0] - 400))
        text_h = text.get_size()[1]
        screen.blit(text,(830,line.center[1] - text_h / 2))

        
        # check for line collision
        if click_down:
            x.update_mouse(pg.mouse.get_pos())


        if click_down and circle_rect.collidepoint(pg.mouse.get_pos()):
            m_w  = round(round(pg.mouse.get_pos()[0]) / 10) * 10
            if 400 <= m_w <= 800:
                circle_center = (m_w,line.center[1])
            # set new fps
            c.FPS = circle_center[0] - 400
            if c.FPS == 0:
                c.FPS = 1
        
        # draw circle on speed line
        pg.draw.circle(screen,(255,255,255),circle_center,15)

        # draw number of elements text
        text = c.NUMBER_TEXT
        text_w = text.get_size()[0]
        screen.blit(text,(c.SCREEN_W / 2 - text_w / 2, 250))

        # draw number of elements line
        line = pg.Rect(400,400,400,4)
        line.center = (line.center[0],text.get_size()[1])

        pg.display.flip()
        main_clock.tick(30)


while True:
    screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                gui_draw()
                cols = Column.get_uniform_cols(c.COL_NO)
                # gen = sorting.quicksort_gen(cols,0,c.COL_NO-1)
                gen = sorting.bubblesort_gen(cols)
    
    update_cols_and_draw(cols,gen,screen)
    pg.display.flip()
    main_clock.tick(c.FPS) 
