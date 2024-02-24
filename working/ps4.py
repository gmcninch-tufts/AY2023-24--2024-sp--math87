import numpy as np
from scipy.optimize import linprog

actual_value = np.array([ 5000, 600, 3500, 6000 ])
sales_price  = np.array([ 24, 76, 43, 754 ])
weight       = np.array([ 75.5, 27, 3.3, 6.7 ])

Aub = np.array([sales_price,weight])
bub = np.array([800,85])

bounds = 4*[(0,1)]

res = linprog((-1)*actual_value, A_ub = Aub, b_ub = bub,bounds = bounds)

##--------------------------------------------------------------------------------

# make the jth standard basis vector of length 'size'
def sbv(j,size):
    return np.array([1.0 if i == j else 0.0 for i in range(size)])

# record the data for the linear program as a dictionary, for ease of passage
lp = { 'obj': actual_value,
       'Aub': Aub,
       'bub': bub,
       'bounds': bounds
      }
      
def branch(specs,lp):
    n = len(lp["obj"])
    
    # each spec is a dictionary {'var': a, 'val': b}
    
    # first, lookup the indices of the variable for each spec
    crates = ['A','B','C','D']
    indices = [ crates.index(spec['var']) for spec in specs ]

    # now create equality constraints for the "specs"
    Aeq = np.array([sbv(index,4) for index in indices])
    beq = np.array([spec['val'] for spec in specs]) 
       
    result = linprog((-1)*lp['obj'], 
                     bounds = lp['bounds'], 
                     A_ub=lp['Aub'], 
                     b_ub=lp['bub'], 
                     A_eq = Aeq, 
                     b_eq = beq)
    
    if result.success:
        return {'obj_value': (-1)*result.fun,
                'solution': result.x}
    else:
        return 'lin program failed'

res_A0 = branch([{'var': 'A', 'val': 0}],lp)

res_A1 = branch([{'var': 'A', 'val': 1}],lp)    

res_A1_D0 = branch([{'var': 'A', 'val': 1},
                    {'var': 'D', 'val': 0}],lp)

res_A1_D1 = branch([{'var': 'A', 'val': 1},
                    {'var': 'D', 'val': 1}],lp)

res_A1_D1_C0 = branch([{'var': 'A', 'val': 1},
                       {'var': 'D', 'val': 1},
                       {'var': 'C', 'val': 0}],lp)


res_A1_D1_C1 = branch([{'var': 'A', 'val': 1},
                       {'var': 'D', 'val': 1},
                       {'var': 'C', 'val': 1}],lp)


res_A1_D1_C0_B0 = branch([{'var': 'A', 'val': 1},
                          {'var': 'D', 'val': 1},
                          {'var': 'C', 'val': 0},
                          {'var': 'B', 'val': 0}],lp)

res_A1_D1_C0_B1 = branch([{'var': 'A', 'val': 1},
                          {'var': 'D', 'val': 1},
                          {'var': 'C', 'val': 0},
                          {'var': 'B', 'val': 1}],lp)

res_A0_B0 = branch([{'var': 'A', 'val': 0},
                    {'var': 'B', 'val': 0}],lp)

res_A0_B1 = branch([{'var': 'A', 'val': 0},
                    {'var': 'B', 'val': 1}],lp)


from graphviz import Graph

nodes = { 0: res.fun,
          1: res_A0['obj_value'],
          2: res_A1['obj_value'],
          3: res_A1_D0['obj_value'],
          4: res_A1_D1['obj_value'],
          5: res_A1_D1_C0['obj_value'],
          7: res_A1_D1_C0_B0['obj_value'],
          }

pruned = [1,3,6,8]

def describe(n):
    if n in nodes.keys():
        if n in pruned:
            return f"{nodes[n]:.2f}\n **pruned**"
        else:
            return f"{nodes[n]:.2f}"
    else:
        return "infeas\n **pruned**"

dot = Graph()
dot.filename='PS4--tree'
dot.format='png'


for n in range(9):
    dot.node(f"{n}",describe(n))
    
dot.edge('0','1','A=0')
dot.edge('0','2','A=1')
dot.edge('2','3','D=0')
dot.edge('2','4','D=1')
dot.edge('4','5','C=0')
dot.edge('4','6','C=1')
dot.edge('5','7','B=0')
dot.edge('5','8','B=1')

dot.render()
