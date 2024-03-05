import numpy as np
import sympy as sp
from numpy.linalg import matrix_power

A = np.array([[1,0],[0.8,0.5]])
B = np.array([[0.5,0],[0.8,0.4]])

w = np.array([1,1])

pn,po = sp.symbols('pn po')

p = np.array([pn,po])

def tot(mat,years):
    return w @ sum([matrix_power(mat,j) @ p for j in range(years)])

print(tot(A,4))
print(tot(B,4))
