def bubblesort_gen(columns):
    '''Generator for bubblesort'''
    ok = False
    while not ok:
        ok = True
        for i in range(1,len(columns)):
            if columns[i].value < columns[i-1].value:
                columns[i].swap(columns[i-1])
                ok = False
                columns[i].highlight = True
                yield columns
                columns[i].highlight = False



def quicksort_gen(columns, lo, hi):
    '''Generator for quicksort'''
    def partition(columns, lo, hi):
        d = 0
        while lo < hi:
            if columns[lo] > columns[hi]:
                columns[lo].swap(columns[hi])
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
