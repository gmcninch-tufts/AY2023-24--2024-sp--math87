---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

Math087 - Mathematical Modeling
===============================
[Tufts University](http://www.tufts.edu) -- [Department of Math](http://math.tufts.edu)  
[George McNinch](http://gmcninch.math.tufts.edu) <george.mcninch@tufts.edu>  
*Fall 2020*

Course material: Bi-partite graphs - code and data for problem set 5
----------------------------------------------------------------------------

```python
import numpy as np
from scipy.optimize import linprog
from itertools import product

## the function find_matching defined below finds a maximal matching
## for a bi-partite graph

## the graph is given by 3 pieces of data: a set `U`, a set `W`, and a
## set `edge` of pairs (u,v) in the product U x V

## the matching is found by solving a linear program. Recall that we
## first associate a directed graph to the bi-partite graph, and solve
## the ``max-flow`` linear program for that directed graph.

def sbv(index,size):
    return np.array([1.0 if i == index else 0.0 for i in range(size)])

def to_vector(l,X):
    ## argument X is a list, and l is a list of elements from X.
    ## suppose that l=[x1,x2,...,xm] and suppose that
    ## n1,n2,...,nm are the indices of the xi in the list X.
    ## 
    ## this function returns the sum of the standard basis vectors
    ## sbv(ni,#X) for i =1,...,m
    ii = map(X.index,l)
    return sum([sbv(i,len(X)) for i in ii],np.zeros(len(X)))

def find_matching(U,W,edges):
    UW = list(product(U,W))

    edge_dict = {(u,w):True if (u,w) in edges else False for (u,w) in UW}
    
    def U_node(x):
        # compute the row-vector corresponding to the conservation law
        # for nodes in U the directed graph has an edge s -> u for
        # each u in U, and an edge w -> t for each w in W, as well as
        # the edges u->w coming from the original bi-partite graph.
        # Thus the rows of the constraint matrix for the linear program
        # have length #U + (#U)(#W) + #W
        return np.block([to_vector([x],U),
                         (-1)*to_vector([(x,w) for w in W if edge_dict[(x,w)]],UW),
                         np.zeros(len(W))])
                     

    def W_node(x):
        # compute the row-vector corresponding to the conservation law for a node in W
        # this row again has length #U + (#U)(#W) + #W.
        return np.block([np.zeros(len(U)),
                         (-1)*to_vector([(u,x) for u in U if edge_dict[(u,x)]],UW),
                         to_vector([x],W)])

    ## construct the equality constraint matrix from conservation laws
    A = np.array([U_node(x) for x in U] + [W_node(x) for x in W])

    ## construct the row for the objective function
    c = np.block([np.ones(len(U)), np.zeros(len(UW)), np.zeros(len(W))])

    lp_result = linprog((-1)*c,
                        A_eq=A,
                        b_eq=np.zeros(len(U) + len(W)),
                        bounds=(0,1),
                        method='revised simplex')

    def compare(r,targ=0,ee=1e-5):
        return True if np.abs(r-targ)<ee else False

    def extract(vec):
        pv = [vec[k + len(U)] for k in range(len(UW))]
        ## our optimal solution "should" have all entries either 0 or 1.
        ## if that isn't so, we raise an exception.
        test = [True if compare(x,1) or compare(x,0) else False for x in pv]
        if all(test):
            match = [(u,w)  for (u,w) in UW if compare(pv[UW.index((u,w))],1)]
            return match
        else:
            raise Exception("linprog solution not of correct form.")

    match=extract(lp_result.x)
    
    if lp_result.success:
        return match
    else:
        raise Exception("linprog failed")
    

def display_matching(U,W,edges):
    UW = list(product(U,W))
    match = find_matching(U,W,edges)
    l = [f"length of matching: {len(match)}"] 
    s = [f"{u}  ---> {w}" for (u,w) in match]
    return "\n".join(l+s)


```

```python
U = ['a','b','c','d','e','f','g','h','i','j','k']
W = ['A','B','C','D','E','F','G','H','I','J','K']

edges = [('a', 'A'), ('b', 'A'), ('c', 'B'), ('c', 'K'), 
         ('e', 'F'), ('e', 'G'), ('f', 'C'), ('f', 'G'), 
         ('f', 'H'), ('f', 'I'), ('f', 'J'), ('f', 'K'), 
         ('g', 'A'), ('g', 'E'), ('g', 'H'), ('h', 'B'), 
         ('h', 'D'), ('h', 'E'), ('h', 'F'), ('h', 'J'), 
         ('k', 'D'), ('k', 'I')]

print(display_matching(U,W,edges))

```

```python
print(display_matching(U,W,product(U,W)))
```

```python
list(product([1,2,3],[4,5]))
```

```python

```
