import copy


def bubblesort_gen(columns,lo,hi):
    '''Generator for bubblesort'''
    ok = False
    while not ok:
        ok = True
        for i in range(lo+1,hi+1):
            if columns[i] < columns[i-1]:
                columns[i].swap_value(columns[i-1])
                ok = False
                columns[i].highlight = True
                yield columns
                columns[i].highlight = False

def selectionsort_gen(columns,lo,hi):
    '''Generator for selectionsort'''
    for i in range(lo,hi+1):
        idx_mini = i
        columns[i].color = (255, 230, 51)
        for j in range(i+1,hi+1):
            if columns[idx_mini] > columns[j]:
                columns[j].color = (0,255,0)
                if idx_mini != i:
                    columns[idx_mini].color = (255,255,255)
                idx_mini = j
                yield columns
            else:
                columns[j].color = (255,0,0)
                yield columns
                columns[j].color = (255,255,255)
            
        columns[i].color = (255,255,255)
        columns[idx_mini].color = (255,255,255)
        if columns[idx_mini] != columns[i]:
            columns[i].swap_value(columns[idx_mini])
            yield columns

def insertionsort_gen(columns,lo,hi):
    '''Generator for insertionsort'''
    for i in range(lo+1,hi+1):
        x = copy.deepcopy(columns[i])
        j = i - 1
        while j >= lo and columns[j] > x:
            columns[j+1].value = columns[j].value
            j -= 1
            yield columns
        columns[j+1] = x
        yield columns

def quicksort_gen(columns, lo, hi):
    '''Generator for quicksort'''
    def partition(columns, lo, hi):
        d = 0
        while lo < hi:
            if columns[lo] > columns[hi]:
                columns[lo].swap_value(columns[hi])
                yield columns
                d = 1 - d
            lo += d
            hi -= 1 - d
        yield lo

    if lo < hi:
        for state in partition(columns, lo, hi):
            if isinstance(state,list):
                yield state
            else:
                p = state
        for state in quicksort_gen(columns,lo,p-1):
            yield state
        for state in quicksort_gen(columns,p+1,hi):
            yield state

def mergesort_gen(columns,lo,hi):
    if lo < hi:
        mid = (lo + hi) // 2
        for state in mergesort_gen(columns,lo,mid): yield state
        for state in mergesort_gen(columns,mid+1,hi): yield state
        aux = []
        i,j = lo,mid+1
        while i <= mid and j <= hi:
            if columns[i] < columns[j]:
                aux.append(columns[i].value)
                i += 1
            else:
                aux.append(columns[j].value)
                j += 1
        aux.extend([x.value for x in columns[i:mid+1]])
        aux.extend([x.value for x in columns[j:hi+1]])
        for i in range(lo,hi+1):
            columns[i].color = (0,255,0)
            columns[i].value = aux[i-lo]
            yield columns
    for i in range(lo,hi+1):
        columns[i].color = (255,255,255)
       

sort_gen = [bubblesort_gen,selectionsort_gen,insertionsort_gen,quicksort_gen,mergesort_gen]