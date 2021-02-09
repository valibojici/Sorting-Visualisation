import constants as c
import pygame as pg
import random
from math import floor,ceil

pg.init()

class Column:
    '''Class for column shapes'''
    def __init__(self,index,value,color=(255,255,255)):
        self.value = value
        self.index = index
        self.color = color
        self.highlight = False

    def __repr__(self):
        return f'Column({self.index},{self.value},{self.color})'

    def __lt__(self,other):
        return self.value < other.value

    def draw(self,surface,color=None):
        '''Draws self on surface'''
        column = pg.Rect(
            self.index*c.COL_W,c.SCREEN_H - self.value,
            c.COL_W-1,self.value+1
            )
        color = color if color is not None else self.color
        if self.highlight:
            color = (0,255,0)
        pg.draw.rect(surface,color,column)

    def swap(self,other):
        '''Swaps value with other'''
        self.value, other.value = other.value, self.value

    @classmethod
    def get_random_cols(cls,min_val,max_val,size):
        '''Get list of columns with random values'''
        aux = [random.randint(min_val,max_val) for _ in range(size)]
        return [Column(idx,val) for idx,val in enumerate(aux)]

    @classmethod
    def get_uniform_cols(cls,size):
        '''Get shuffled list of columns with constant increment'''
        incr = round((c.SCREEN_H - 1) / (size - 1),3)
        aux = [1 + round(incr*i,1) for i in range(size)]
        random.shuffle(aux)
        return [Column(idx,x) for idx,x in enumerate(aux)]
