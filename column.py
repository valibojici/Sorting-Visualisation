import constants as c
import pygame as pg
import random

pg.init()

class Column:
    '''Class for column shapes'''
    def __init__(self,index,value,color=(255,255,255)):
        self.value = value
        self.index = index
        self.color = color

    def __repr__(self):
        return f'Column({self.index},{self.value},{self.color})' 

    def draw(self,surface,color=None):
        '''Draws self on surface'''
        column = pg.Rect(
            self.index*c.COL_W,c.SCREEN_H - self.value,
            c.COL_W-1,self.value+1
            )
        color = color if color is not None else self.color
        pg.draw.rect(surface,self.color,column)

    @classmethod
    def get_random_cols(cls,min_val,max_val,size):
        '''Get list of columns with random values''' 
        aux = [random.randint(min_val,max_val) for _ in range(size)]
        return [Column(idx,val) for idx,val in enumerate(aux)]

    @classmethod
    def get_uniform_cols(cls,size):
        '''Get shuffled list of columns with constant increment'''
        incr = (c.SCREEN_H - 1) / (size - 1)
        aux = [Column(idx,1 + incr*idx) for idx,x in enumerate(range(1,size+1))]
        random.shuffle(aux)
        return aux
