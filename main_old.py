import pygame as pg
import random
pg.init()

WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH,HEIGHT))
running = True
col_width = 5
no_cols = WIDTH // col_width
fps = 60
fps_clock = pg.time.Clock()

class Column:
    col_width = 4

    def __init__(self,idx,value,color = (255,255,255)):
        self.val = value
        self.idx = idx
        self.color = color

    def __repr__(self):
        return f'Column({self.idx},{self.val})'

    def __lt__(self, other):
        return self.val < other.val

    # def __eq__(self, other):
    #     return self.val == other.val

    def draw(self,surface):
        rect = pg.Rect(self.idx * col_width, HEIGHT - self.val, col_width - 1, self.val + 1)
        pg.draw.rect(surface,self.color,rect)

    def swap(self,other):
        self.val,other.val = other.val, self.val


def get_random_nums():
    nums = [round(x * (HEIGHT / no_cols), 1) for x in range(1,no_cols+1)]
    random.shuffle(nums)

    return [Column(idx,num) for idx,num in enumerate(nums)]
    # hello

def bubble_sort(nums):
    for i in range(len(nums)-1):
        for j in range(i+1,len(nums)):
            if nums[i] > nums[j]:
                nums[i].swap(nums[j])
                yield nums

def insertion_sort(nums):
    for i in range(1,len(nums)):
        j = i - 1
        num = nums[i].val
        while j >= 0 and nums[j] > num:
            nums[j+1].val = nums[j].val
            j -= 1
            yield nums
        nums[j+1].val = num
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
                aux.append(nums[i].val)
                i+=1
            else:
                aux.append(nums[j].val)
                j+=1
        aux.extend(x.val for x in nums[i:mid+1])
        aux.extend(x.val for x in nums[j:hi+1])
        for i in range(lo,hi+1):
            nums[i].color = (0,255,0)
            nums[i].val = aux[i-lo]
            yield nums
    for k in range(lo, hi + 1):
        nums[k].color = (255, 255, 255)


def quicksort(nums, lo, hi):

    def partition(nums,lo,hi):
        d = 0
        while lo < hi:
            if nums[hi] < nums[lo]:
                nums[hi].swap(nums[lo])
                nums[hi].color = nums[lo].color = (255,0,0)
                d = 1-d
                yield nums
                nums[hi].color = nums[lo].color = (255,255,255)
            lo += d
            hi -= 1-d
        yield lo

    if lo < hi:
        for state in partition(nums,lo,hi):
            if isinstance(state,list):
                yield state
            else:
                p = state
        nums[p].color = (100,0,0)
        for state in quicksort(nums,lo, p-1):
            yield state
        for state in quicksort(nums,p+1,hi):
            yield state
        nums[p].color = (255,255,255)
    yield nums

nums = get_random_nums()
gen = quicksort(nums,0,len(nums)-1)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            nums = get_random_nums()
            gen = merge_sort(nums, 0, len(nums) - 1)
    for num in nums:
        num.draw(screen)
    try:
        nums = next(gen)
    except StopIteration:
        pass
    pg.display.flip()
    screen.fill((0,0,0))
    fps_clock.tick(fps)
