import numpy as np
from scipy.optimize import bisect, newton

## functions we'll use as examples

def f(x):
    return x**2 - x - 1

def fprime(x):
    return 2*x - 1

def h(x):
    return 1 - np.log(x)

def hprime(x):
    return -1/x


roots_for_f = {"bisect": np.array([bisect(f,1,2),
                                   bisect(f,-2,0)]),
               "secant": np.array([newton(f,1,x1=2),
                                   newton(f,-1,x1=-2)]),
               "newton": np.array([newton(f,1,fprime),
                                   newton(f,-1,fprime)]),
               "via_radicals": np.array([(1+np.sqrt(5))/2,
                                         (1-np.sqrt(5))/2 ])}

roots_for_sin = {"bisect": bisect(np.sin,1,4),
                 "secant": newton(np.sin,1.0,x1=4.0),
                 "newton": newton(np.sin,2.0,fprime=np.cos)}


roots_for_h = {"bisect": bisect(h,1,3),
               "secant": newton(h,2,x1=3),
               "newton": newton(h,3,fprime=hprime)}


def report(dict):
    return "\n".join(map(lambda k: f"{k:12s} :: {dict[k]}",dict))


print("roots for f:")
print(report(roots_for_f))

print("roots for sin:") 
print(report(roots_for_sin))

print("roots for h:")
print(report(roots_for_h))

