import numpy as np


from scipy.optimize import linprog

c = np.array([11,5])

A = np.array([[1,1],[10,4]])

b = np.array([7,40])

primal = linprog((-1)*c,A_ub = A, b_ub = b)

dual = linprog(b,A_ub = (-1)*A.T, b_ub = (-1)*c)

print("primal: \n", primal,"\n")
print("dual: \n",dual)

print(abs(primal.fun) == abs(dual.fun))


def deltaB(x):
    return np.array([x,0])


def get_optimal(d):
    result = linprog((-1)*c, A_ub=A, b_ub = b + deltaB(d))
    s1 = f"d = {d}: x + y <= {7+d}, x' = {abs(result.fun):.2f}"
    s2 = f"x* + Δb @ dual.x = {abs(primal.fun) + deltaB(d) @ dual.x}"
    return s1 + s2

from pprint import pprint
pprint([ get_optimal(d) for d in [1,2,4]])
