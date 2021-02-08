import pygame as pg
import random
pg.init()
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH,HEIGHT))
running = True
col_width = 4
no_cols = WIDTH // col_width

fps = 30
fps_clock = pg.time.Clock()


def draw_rect(surface,idx,num):
    rect = pg.Rect(idx*col_width, HEIGHT - num, col_width-1, num+1)
    pg.draw.rect(surface,(255,255,255),rect)

def bubble_sort(nums):
    for i in range(len(nums)-1):
        for j in range(i+1,len(nums)):
            if nums[i] > nums[j]:
                nums[i],nums[j] = nums[j],nums[i]
                yield nums


def insertion_sort(nums):
    for i in range(1,len(nums)):
        j = i - 1
        num = nums[i]
        while j >= 0 and nums[j] > num:
            nums[j+1] = nums[j]
            j -= 1
            yield nums
        nums[j+1] = num
        yield nums


def merge_sort(nums,lo,hi):
    if lo < hi:
        mid = lo + (hi - lo) // 2
        aux_gen = merge_sort(nums,lo,mid)
        for state in aux_gen:
            yield state

        aux_gen = merge_sort(nums,mid+1,hi)
        for state in aux_gen:
            yield state

        aux = []
        i,j = lo, mid+1
        while i <= mid and j <= hi:
            if nums[i] < nums[j]:
                aux.append(nums[i])
                i+=1
            else:
                aux.append(nums[j])
                j+=1
        aux.extend(nums[i:mid+1])
        aux.extend(nums[j:hi+1])
        for i in range(lo,hi+1):
            nums[i] = aux[i-lo]
            yield nums


def quicksort(nums, lo, hi):

    def partition(nums,lo,hi):
        d = 0
        while lo < hi:
            if nums[hi] < nums[lo]:
                nums[hi],nums[lo] = nums[lo],nums[hi]
                d = 1-d
                yield nums
            lo += d
            hi -= 1-d
        yield lo

    if lo < hi:
        for state in partition(nums,lo,hi):
            if isinstance(state,list):
                yield state
            else:
                p = state
        for state in quicksort(nums,lo, p-1):
            yield state
        for state in quicksort(nums,p+1,hi):
            yield state
    yield nums

# nums = [random.randint(1,HEIGHT) for _ in range(WIDTH // col_width)]
nums = [round(x*(HEIGHT / no_cols),1) for x in range(no_cols)]
random.shuffle(nums)
gen = quicksort(nums,0,len(nums)-1)
# gen = bubble_sort(nums)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            nums = [round(x * (HEIGHT / no_cols), 1) for x in range(no_cols)]
            random.shuffle(nums)
            gen = quicksort(nums, 0, len(nums) - 1)
    for idx,num in enumerate(nums):
        draw_rect(screen,idx,num)
    try:
        nums = next(gen)
    except(StopIteration):
        pass
    pg.display.flip()
    screen.fill((0,0,0))
    fps_clock.tick(fps)

