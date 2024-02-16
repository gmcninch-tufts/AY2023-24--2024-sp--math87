
import numpy as np
from scipy.optimize import linprog

bag_specs = { 'A' : { 'price': 12.0,
                      'cupcakes': 4,
                      'cookies': 2,
                      'bags': 1
                      },
              'B' : { 'price': 16.0,
                      'cupcakes': 2,
                      'cookies': 5,
                      'bags': 1
                      }
              }

resources = { 'cupcakes': 115.0,
              'cookies': 90.0,
              'bags': 45
             }

# build the (0-indexed) standard basis vector
# e.g. sbv(2,4) returns [ 0.0, 0.0, 1.0, 0.0 ]
#
def sbv(index,len):
    return np.array([ 1.0 if index == i else 0.0 for i in range(len) ])

# return the standard basis vector corresponding to the index of an entry in a list
# e.g. itemVector('b',['a','b','c','d']) returns [ 0.0, 1.0, 0.0, 0.0 ]
#


# objective function, as a vector
obj = np.array([ bag_specs[item]['price'] for item in bag_specs.keys() ])

# upper bound constraint matrix
Aub = np.array([ [ bag_specs[item][resource]
                   for item in bag_specs.keys()
                  ]
                 for resource in resources.keys()
                ])

# upper bound constraint vector
bub = np.array([ resources[res] for res in resources.keys()])

# remember that this is a maximizing problem, so multiply the objective function by (-1)
#
res = linprog( (-1)*obj, A_ub = Aub, b_ub = bub)


# # print(obj)

# # print(Aub)

# # print(bub) 

# # print(res)


# pp = [ [24,8], [24,9], [25,8], [25,9] ]


# print("\n".join([ f"{p} => {Aub @ np.array(p)}   {Aub @ np.array(p) <= bub}" for  p in pp ]))


