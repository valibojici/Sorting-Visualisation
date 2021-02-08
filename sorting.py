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