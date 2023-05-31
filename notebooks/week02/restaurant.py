import numpy as np
from networkflows import Edge,LowerBound,UpperBound,networkFlow
import math
import scipy.optimize

tt = np.array([10,10,15,20,40,40,30])

clean = [ f"d{d} clean" for d in range(7) ]
used  = [ f"d{d} used"  for d in range(7) ]

vv = [['source'], clean, used]


ee = [*[ Edge(('source',clean[d]),   label=f"b{d}", val=5) # bought
         for d in range(7)
        ],   
      *[ Edge((clean[d],used[d]),    label=f"u{d}", bd=LowerBound(tt[d])) # usage
         for d in range(7)
        ],  
      *[ Edge((clean[d],clean[d+1]), label=f"c{d}" )       # carry-over
        for d in range(6)
       ],  
      *[ Edge((used[d],clean[d+1]),  label=f"f{d}", val=2) # fast laundry
        for d in range(6)
       ], 
      *[ Edge((used[d],clean[d+2]),  label=f"s{d}", val=1) # slow laundry
        for d in range(5)
       ]
      ]

def report(nf: networkFlow) -> str:
    lp=nf.runLinProgr()
    x = lp.x
    costs = lp.fun
    return "\n".join(
        [f"linprog succeeded? {lp.success}",
         f"Optimal tablecloth expenses for the week are ${costs:.2f}",
         "This is achieved by the following strategy:",
         *[f"purchase on day {i}: {x[i]:.2f}" for i in range(7)],
         "",
         *[f"use on day {i}: {x[7+i]:.2f}" for i in range(7)],
         "",
         *[f"carry-over from day {i} to day {i+1}: {x[14+i]:.2f}" for i in range(6)],
         "",
         *[f"fast laundry on day {i}: {x[20+i]:.2f}" for i in range(6)],
         "",
         *[f"slow laundry on day {i}: {x[26+i]:.2f}" for i in range(5)],
         ])
        


nf = networkFlow(vv,ee,title="Restaurant",source='source',sink='d6 used')

nf.makeGraph().render()

print(report(nf))
