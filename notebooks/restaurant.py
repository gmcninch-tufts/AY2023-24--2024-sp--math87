import numpy as np
from digraph import Edge,LowerBound,UpperBound,networkFlow
import math

import scipy.optimize
import itertools

tt = np.array([10,10,15,20,40,40,30])

clean = [ f"d{d} clean" for d in range(7) ]
used  = [ f"d{d} used"  for d in range(7) ]

vv = [['source'], clean, used]


ee = [*[ Edge(('source',clean[d]),        # bought
              label=f"b{d}",
              val=5)
         for d in range(7)
        ],   
      *[ Edge((clean[d],used[d]),         # usage
              label=f"u{d}",
              bd=LowerBound(tt[d]))
         for d in range(7)
        ],  
      *[ Edge((clean[d],clean[d+1]),      # carry-over
             label=f"c{d}" )
        for d in range(6)
       ],  
      *[ Edge((used[d],clean[d+1]),       # fast laundry
             label=f"f{d}",
             val=2)
        for d in range(6)
       ], 
      *[ Edge((used[d],clean[d+2]),       # slow laundry
             label=f"s{d}",
             val=1)
        for d in range(5)
       ]
      ]

def report(result: scipy.optimize.OptimizeResult) -> str:
    """the argument ``result`` should be an instance of the class ``scipy.optimize.OptimizeResult`` -- 
    i.e. a value of the form returned by ``linprog``
    """
    x = result.x
    costs = result.fun
    return "\n".join(
        [f"linprog succeeded? {result.success}",
         f"Optimal tablecloth expenses for the week are ${costs:.2f}",
         "This is achieved by the following strategy:",
         *[f"purchase on day {i}: {x[i]:.2f}" for i in range(7)],
         "",
         *[f"use on day {i+1}: {x[6+i]:.2f}" for i in range(7)],
         "",
         *[f"carry-over from day {i} to day {i+1}: {x[13+i]:.2f}" for i in range(6)],
         "",
         *[f"fast laundry on day {i}: {x[19+i]:.2f}" for i in range(6)],
         "",
         *[f"slow laundry on day {i}: {x[19+i]:.2f}" for i in range(5)],
         ])
        


nf = networkFlow(vv,ee,title="Restaurant",source='source',sink='d6 used')

nf.drawGraph().render()

lp = nf.runLinProgr()
print(report(lp))
