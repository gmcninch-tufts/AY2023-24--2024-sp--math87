import numpy as np
from scipy.optimize import linprog

from pprint import pprint

c = np.array([9,5])

A = np.array([[1,1],[12,5]])

b = np.array([50 , 60])

primal  = linprog((-1)*c,A_ub = A, b_ub = b)

dual = linprog(b,A_ub = (-1)*A.T, b_ub = (-1)*c)

print("primal: \n", primal,"\n")
print("dual: \n",dual)


def deltaB(d):
    return np.array([d,0])

def compare(c,A,b,d):
    primal  = linprog((-1)*c,A_ub = A, b_ub = b)
    dual    = linprog(b,A_ub = (-1)*A.T, b_ub = (-1)*c)
    tweaked = linprog((-1)*c, A_ub=A, b_ub = b + deltaB(d))
    print(b+deltaB(d))
    s1 = f"d = {d}: x_1 + x_2 <= {50+d}, c @ x' = {abs(tweaked.fun):.2f}"
    s2 = f"c @ x* + Δb @ dual.x = {abs(primal.fun) + deltaB(d) @ dual.x}"
    return s1 + ", " + s2

results = [ compare(c,A,b,d) for d in range(0,10,2) ]

pprint(results)
