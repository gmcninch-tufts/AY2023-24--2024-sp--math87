import numpy as np
from scipy.optimize import linprog


## requirements per acre
crop_specs = { 'wheat' : { 'profits': 200.0,
                           'workers': 3,
                           'fertilizer': 2,
                           'acres': 1
                          },
               'corn' : { 'profits': 300.0,
                          'workers': 2,
                          'fertilizer': 4,
                          'acres': 1
                         }
              }

crops = [ c for c in crop_specs.keys() ]

resource_specs = { 'workers': 100.0,
                   'fertilizer': 120.0,
                   'acres': 45
                  }

resources = [ r for r in resource_specs.keys() ]

# build the (0-indexed) standard basis vector
# e.g. sbv(2,4) returns [ 0.0, 0.0, 1.0, 0.0 ]
#
def sbv(index,len):
    return np.array([ 1.0 if index == i else 0.0 for i in range(len) ])

# return the standard basis vector corresponding to the index of an entry in a list
# e.g. itemVector('b',['a','b','c','d']) returns [ 0.0, 1.0, 0.0, 0.0 ]
#
def itemVector(x,ll):
    return sbv(ll.index(x),len(ll))

# objective function, as a vector
obj = np.array([ crop_specs[c]['profits'] for c in crop_specs.keys() ])

# upper bound constraint matrix
Aub = np.array([ [ crop_specs[c][res]
                   for c in crop_specs.keys()
                  ]
                 for res in resource_specs.keys()
                ])

# upper bound constraint vector
bub = np.array([ resource_specs[res] for res in resource_specs.keys()])

res = linprog( (-1)*obj, A_ub = Aub, b_ub = bub)

print(obj)

print(Aub)

print(bub) 

print(res)


usage = Aub @ np.array([20,20])

for r in resources:
    print(f"{r} -> {usage[resources.index(r)]}")
