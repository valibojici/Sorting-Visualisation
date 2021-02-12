import constants as c
import pygame as pg
import random

pg.init()

class Column:
    '''Class for column shapes'''
    def __init__(self,value,color=(255,255,255)):
        self.value = value
        self.color = color
        self.highlight = False

    def __repr__(self):
        return f'Column({self.value},{self.color})'

    def __lt__(self,other):
        return self.value < other.value

    def draw(self,surface,index,color=None):
        '''Draws self on surface'''
        column = pg.Rect(
            index*c.COL_W,c.SCREEN_H - self.value,
            c.COL_W-1,self.value+1,
            )
        pg.draw.rect(surface,color if color else self.color,column)

    def swap_value(self,other):
        self.value,other.value = other.value, self.value
    @classmethod
    def get_random_cols(cls,min_val,max_val,size):
        '''Get list of columns with random values'''
        return [Column(val) for val in [random.randint(min_val,max_val) for _ in range(size)]]

    @classmethod
    def get_uniform_cols(cls,size):
        '''Get shuffled list of columns with constant increment'''
        incr = (c.SCREEN_H/ size)
        aux = [incr*i for i in range(1,size+1)]
        random.shuffle(aux)
        return [Column(val) for val in aux]
        