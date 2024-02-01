int_pts = [ (4,9), (8,9), (10,5), (8,1), (4,1), (2,5) ]
	  
def f(x,y): return x + 2*y
	  
a=[ (f(pt[0],pt[1]),pt) for pt in int_pts]

a.sort()

import numpy as np
c = np.array([1,2])

Aub = np.array([ [0,1],
	         [0,-1],
		 [2,1],
		 [-2,-1],
		 [-2,1],
		 [2,-1]
		])
	  
bub = np.array([ 9,
	         -1,
		 25,
		 -9,
		 1,
		 15])
					  

from scipy.optimize import linprog
res=linprog((-1)*c,A_ub=Aub,b_ub=bub)
