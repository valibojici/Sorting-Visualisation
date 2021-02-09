import pygame as pg 
pg.init()

SCREEN_W = 1200
SCREEN_H = 600
FPS = 30
COL_NO = 200
COL_W = round(SCREEN_W / COL_NO,5)


FONT = pg.font.SysFont("Arial.ttf",50)

SORT_TEXT = [
    FONT.render('Bubble Sort', True, (255,255,255)),
    FONT.render('Selection Sort', True, (255,255,255)),
    FONT.render('Insertion Sort', True, (255,255,255)),
    FONT.render('Quick Sort', True, (255,255,255)),
    FONT.render('Merge Sort', True, (255,255,255))
]

SPEED_TEXT = FONT.render('Speed', True, (255,255,255))
NUMBER_TEXT = FONT.render('Number of elements', True, (255,255,255))
SPEED_VAL = {
    val : FONT.render(str(1 if val == 0 else val) + " FPS", True, (255,255,255)) for val in range(0,401,10)
}