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
                columns[i].color = (0,255,0)
                yield columns
                columns[i].color = (255,255,255)

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
        columns[i].color = (0,255,0)
        yield columns
        columns[i].color = (255,255,255)
        j = i - 1
        while j >= lo and columns[j] > x:
            columns[j+1].value = columns[j].value

            columns[j+1].color = (255, 230, 51)
            yield columns
            columns[j+1].color = (255,255,255)

            j -= 1
        columns[j+1] = x
        columns[j+1].color = (0,255,0)
        yield columns
        columns[j+1].color = (255,255,255)

def quicksort_gen(columns, lo, hi):
    '''Generator for quicksort'''
    def partition(columns, lo, hi,*, pivot=False):
        L,H = lo,hi
        columns[lo].color = columns[hi].color = (255, 230, 51)
        d = 0
        while lo < hi:
            if columns[lo] > columns[hi]:
                columns[lo].swap_value(columns[hi])
                if not pivot:
                    yield columns
                d = 1 - d
            lo += d
            hi -= 1 - d
        if pivot:
            yield lo
        columns[L].color = columns[H].color =  (255,255,255)

    if lo < hi:
        columns_2 = copy.deepcopy(columns)
        p = partition(columns_2,lo,hi,pivot=True)
        p = next(p)
        columns[p].color =  (255, 0, 0)
        for state in partition(columns,lo,hi,pivot=False):
            yield state
        columns[p].color = (255,255,255)

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


def heapsort_gen(columns,lo,hi):
    def heap_down(idx,hi):
        
        def idx_child_max(idx,hi):
            if idx * 2 + 2 <= hi:
                return idx * 2 + 1 if columns[idx*2+1] > columns[idx*2+2] else idx * 2 + 2
            return idx * 2 + 1

        if idx <= (hi-1) // 2:
            idx_child = idx_child_max(idx,hi)
            child_color = columns[idx_child].color

            columns[idx].color = (255,0,0)
            columns[idx_child].color = (255,150,150)
            yield columns
            columns[idx].color = (255,255,255)
            columns[idx_child].color = child_color

            if columns[idx] < columns[idx_child]:
                columns[idx].swap_value(columns[idx_child])
                
                columns[idx_child].color = (255,0,0)
                yield columns
                columns[idx_child].color = child_color

                for state in heap_down(idx_child,hi):
                    yield state

    def heapify():
        # leaves
        for i in range((hi-1)//2 + 1, hi+1):
            columns[i].color = (143, 132, 209)
        yield columns

        for i in range(len(columns)//2 - 1,-1,-1):
            for state in heap_down(i,hi):
                yield state

    for state in heapify():
        yield state
    
    for i in range(hi,lo,-1):
        columns[lo].color = (100,200,100)
        yield columns
        columns[lo],columns[i] = columns[i],columns[lo]
        yield columns
        columns[lo].color = (255,0,0)
        yield columns

        # leaves
        for k in range((i-2)//2 + 1, i):
            columns[k].color = (143, 132, 209)
        yield columns

        for state in heap_down(lo,i-1):
            yield state

    for i in range(lo,hi+1):
        columns[i].color = (255,255,255)
        yield columns


def radixsort64_gen(columns,lo,hi):
    for col in columns:
        col.value = round(col.value)
    POWER = 6
    BASE = 2 ** POWER
    count = []
    output = [0 for _ in range(len(columns))]
    shift = steps = 0
    while shift < 32 // POWER:
        count = [0 for _ in range(BASE)]

        for i in range(lo,hi+1):
            count[(columns[i].value >> steps) & (BASE - 1)] += 1

        for i in range(1,BASE):
            count[i] += count[i-1]

        for i in range(hi,lo-1,-1):
            index = (columns[i].value >> steps) & (BASE - 1)
            output[count[index]-1] = columns[i].value
            count[index] -= 1

        for i in range(lo,hi+1):
            columns[i].value = output[i]
            yield columns
        shift += 1
        steps += POWER


def radixsort10_gen(columns,lo,hi):
    for col in columns:
        col.value = round(col.value)
    BASE = 10
    count = []
    output = [0 for _ in range(len(columns))]

    for k in range(0,max([len(str(x.value)) for x in columns])):
        count = [0 for _ in range(BASE)]

        for i in range(lo,hi+1):
            count[(columns[i].value // (10 ** k) ) % BASE] += 1

        for i in range(1,BASE):
            count[i] += count[i-1]

        for i in range(hi,lo-1,-1):
            index = (columns[i].value // (10 ** k) ) % BASE
            output[count[index]-1] = columns[i].value
            count[index] -= 1

        for i in range(lo,hi+1):
            columns[i].value = output[i]
            yield columns



sort_gen = [bubblesort_gen,
            selectionsort_gen,
            insertionsort_gen,
            quicksort_gen,
            mergesort_gen,
            heapsort_gen,
            radixsort64_gen,
            radixsort10_gen
]