
nodes = ['s','a', 'b', 'c', 'd', 't' ]

pp = [ ( ['s'], [13, 16] ),
       ( ['s', 'a'], [13, 10, 12] ),
       ( ['s', 'c'], [16, 4, 14] ),
       ( ['s', 'a', 'c'], [12, 14] ),
       ( ['s', 'a', 'b'], [13, 10, 7, 20] ),
       ( ['s', 'a', 'b', 'c'], [14, 6, 20] ),
       ( ['s', 'a', 'c', 'd'], [12, 7, 4] ),
       ( ['s', 'a', 'b', 'c', 'd'], [4,20])
      ]

def min_cut(data):
    aa = [ (s, sum(cuts) ) for  (s,cuts) in data]
    aa.sort(key=lambda x: x[1])
    return aa
        
pprint(min_cut(pp))


def pp1(x):
    return [ ( ['s'], [13, 16] ),
             ( ['s', 'a'], [13, 10, 12] ),
             ( ['s', 'c'], [16, 4, 14] ),
             ( ['s', 'a', 'c'], [12, 14] ),
             ( ['s', 'a', 'b'], [13, 10, 7, 20] ),
             ( ['s', 'a', 'b', 'c'], [14, 6, 20] ),
             ( ['s', 'a', 'c', 'd'], [12, 7, 4+x] ),
             ( ['s', 'a', 'b', 'c', 'd'], [4+x, 20])
            ]

for c in range(1,5):
    print(f"{c} -> {min_cut(pp1(c))[0]}")
