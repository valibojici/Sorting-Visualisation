import pygame as pg
from math import ceil,floor
pg.init()

class Slider:
    def __init__(self,left,top,width,height,min_val,max_val,start=0,step=1):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.step = round(width / ((max_val - min_val) / step),3)
        self.line_width = height / 8
        self.rect_bound = pg.Rect(left,top,width,height)
        self.center = self.rect_bound.center
        self.line = pg.Rect(left,top+self.height/2-self.line_width/2,width,self.line_width)
        self.circle_center = (Slider.map_value(start,min_val,max_val,left,left+width), self.line.center[1])
    
    def draw(self,surface):
        pg.draw.rect(surface,(255,255,255),self.line)
        pg.draw.circle(surface,(255,255,255),self.circle_center,self.height / 2)

    def debug(self,surface):
        pg.draw.rect(surface,(255,255,255),self.rect_bound,1)

    def update_mouse(self,mouse_pos):
        '''Update slider based on mouse position'''
        if not self.rect_bound.collidepoint(mouse_pos):
            return
        m_w = round(round(mouse_pos[0]) / self.step) * self.step
        m_w = round(m_w,3)
        if self.min_val <= Slider.map_value(m_w,self.left,self.left+self.width,self.min_val,self.max_val) <= self.max_val:
            self.circle_center = (m_w,self.circle_center[1])

    def get_value(self):
        return Slider.map_value(self.circle_center[0],self.left,self.left+self.width,self.min_val,self.max_val)

    @staticmethod
    def map_value(val,minimum,maximum,map_min,map_max):
        return round(((val - minimum)/(maximum - minimum)) * (map_max - map_min) + map_min)