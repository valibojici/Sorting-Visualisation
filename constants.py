import pygame as pg 
pg.init()

SCREEN_W = 1200
SCREEN_H = 600
FPS = 30
COL_NO = 100
COL_W = round(SCREEN_W / COL_NO,4)


FONT = pg.font.SysFont("Arial.ttf",45)

SORT_TEXT = [
    FONT.render('Bubble Sort', True, (255,255,255)),
    FONT.render('Selection Sort', True, (255,255,255)),
    FONT.render('Insertion Sort', True, (255,255,255)),
    FONT.render('Quick Sort', True, (255,255,255)),
    FONT.render('Merge Sort', True, (255,255,255)),
    FONT.render('Heap Sort', True, (255,255,255)),
    FONT.render('Radix Sort (LSD base 64)', True, (255,255,255)),
    FONT.render('Radix Sort (LSD base 10)', True, (255,255,255))
]

SPEED_TEXT = FONT.render('Speed', True, (255,255,255))
NUMBER_TEXT = FONT.render('Number of elements', True, (255,255,255))
# COMPARE_TEXT = FONT.render('Compare', True, (255,255,255))
def GET_TEXT(val):
    return FONT.render(str(val), True, (255,255,255))