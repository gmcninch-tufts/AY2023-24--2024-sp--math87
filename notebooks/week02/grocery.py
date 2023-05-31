import numpy as np
from digraph import Edge,LowerBound,UpperBound,networkFlow
import math

import scipy.optimize
from dataclasses import dataclass, field

months = [ "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "apr", "may", "jun", "jul" ]

@dataclass
class PriceAndDemand:
    month: str
    priceFromGrower: float
    salePrice: float
    demand: int

pdarr = [ PriceAndDemand( "aug" , 0.80 , 0.90 , 10 ),
          PriceAndDemand( "sep" , 0.55 , 0.65 , 15 ),
          PriceAndDemand( "oct" , 0.55 , 0.65 , 15 ),
          PriceAndDemand( "nov" , 0.65 , 0.85 , 15 ),
          PriceAndDemand( "dec" , 0.75 , 1.00 , 13 ),
          PriceAndDemand( "jan" , 0.85 , 1.00 , 10 ),
          PriceAndDemand( "feb" , 0.95 , 1.20 , 10 ),
          PriceAndDemand( "mar" , None , 1.20 , 10 ),
          PriceAndDemand( "apr" , None , 1.20 ,  9 ),
          PriceAndDemand( "may" , None , 1.00 ,  7 ),
          PriceAndDemand( "jun" , None , 0.80 ,  5 ),
          PriceAndDemand( "jul" , None , 0.80 ,  5 )
         ]

def growerSupplies(month: str) -> int:
    if month in ["sep","oct","nov","dec","jan"]:
        return math.inf
    elif month in ["aug","feb"]:
        return 15000
    else:
        return 0


vv = [ ["grower"],
       months,
       ["demand"]
       ]

ee = [ *[Edge(("grower",pd.month),
              label=f"g{months.index(pd.month)}",
              val=-pd.priceFromGrower if pd.priceFromGrower else None,
              bd = UpperBound(growerSupplies(pd.month)))
         for pd in pdarr],                        # purchase from grower
       *[Edge((pd.month,"demand"),
              label=f"d{months.index(pd.month)}",
              val=pd.salePrice,
              bd = UpperBound(pd.demand*1000))
         for pd in pdarr],                        # sales to customers
       *[Edge((pd0.month,pd1.month),
              label=f"s{months.index(pd0.month)}",
              val=-0.025,
              bd = UpperBound(50000))
         for pd0,pd1 in zip(pdarr,pdarr[1:])]     # storage
       ]

def report(res):
    ## the argument ``res`` should be an instance of the class ``scipy.optimize.OptimizeResult`` -- 
    ## i.e. a value of the form returned by ``linprog``
    ##
    x=res.x
    profit  = (-1)*res.fun
    return "\n".join(
        [f"linprog succeeded? {res.success}",
         f"Optimal profit ${profit:.2f}",
         "This is achieved by the following strategy:\n",
         *[f"purchase in kg for {months[i]}: {x[i]:.2f}" for i in range(12)],
         "",
         *[f"sales in kg for {months[i]}: {x[i+12]:.2f}" for i in range(12)],
         "",
         *[f"storage in kg for {months[i]}: {x[i+24]:.2f}" for i in range(11)]
         ])


nf = networkFlow(vv,ee,title="grocery",source="grower",sink="demand")

nf.drawGraph().render()

lp = nf.runLinProgr(maximize=True)
print(report(lp))



