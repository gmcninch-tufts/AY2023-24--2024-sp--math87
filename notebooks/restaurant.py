import digraph

def clean_node(day):
    return f"d{day}c"

def used_node(day):
    return f"d{day}u"

def make_network_model(last):

   dot = Digraph('tablecloth network model')

   dot.attr(rankdir='LR')
   dot.node('s','source of new tablecloths')
   days = range(1,last + 1)

   with dot.subgraph(name='clean') as c:
     c.attr(rank='same')
     for day in days:
        if day == last:
            c.node(clean_node(day),"etc...")
        else:        
            c.node(clean_node(day), f"day {day} clean")

   with dot.subgraph(name='used') as u:
     u.attr(rank='same')
     for day in days:
        if day == last:
            u.node(used_node(day),'etc...')
        else:        
            u.node(used_node(day), f"day {day} used")

   for day in days:
     dot.edge('s',clean_node(day),label='cost=5')
     if day < last:
        dot.edge(clean_node(day),clean_node(day+1), label = "cost=0")

     dot.edge(clean_node(day),used_node(day),label=f"cost=0,ℓ=t_{day}")

     if day < last:
        dot.edge(used_node(day),clean_node(day+1),label="cost=2") ## fast laundry

     if day < last -1:
        dot.edge(used_node(day),clean_node(day+2),label="cost=1") ## slow laundry

   return dot
  
make_network_model(last=5)



#-------------------------------

## This code represents a preliminary implementation
## it just gives the row in the equality constraint corresponding
## to a single row. See the next cell for a "full implementation"

import numpy as np

def sbv(index,length):
    return np.array([1.0 if i == index-1 else 0.0 for i in range(length)])

## produce the row corresponding to the "day 3 clean" node.
##
row = np.block([(-1)*sbv(3,7), ## bb
                 sbv(3,7),       ## uu
                 (-1)*sbv(2,6) + sbv(3,6),  ## cc
                 (-1)*sbv(2,6),       ## ff
                 (-1)*sbv(1,5)       ## ss
               ])

## Note that if you had constructed the following rows -- row1, row2, row3, ..., row7 -- you'd produce the matrix A via
## A = np.array([row1,row2,row3,...,row7])

print(row.shape)
print(row)

## This cell represents one possible way of creating the equality and inquality constraints
## for the "tablecloth" problem

import numpy as np
from scipy.optimize import linprog

float_formatter = "{:.2f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

## "standard basis vector"
##
def sbv(index,size):
    return np.array([1.0 if i == index-1 else 0.0 for i in range(size)])

def from_indices(dat,length):
    ## dat is a list [(c,i).,,,] of pairs; the pair (c,i) determines
    ## the vector c*e_i where e_i is the ith standard basis vector
    ## from_indices(dat,length) function returns the sum of the vectors 
    ## specified by the list dat
    return sum([c*sbv(i,length) for (c,i) in dat],np.zeros(length))

## >>> from_indices([(2,3),(3.5,6)],7)
## array([ 0.,  0., 2., 0.,  0.,  3.5,  0.])

def row(b=[],
        u=[],
        c=[],
        f=[],
        s=[]):
    bb = from_indices(b,7)
    uu = from_indices(u,7)
    cc = from_indices(c,6)
    ff = from_indices(f,6)
    ss = from_indices(s,5)
    return np.block([bb,uu,cc,ff,ss])

## >>> row(bp=[1],un=[2])
## array([ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  0.,  0.,  0.,  0.,
##        0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
##        0.,  0.,  0.,  0.,  0.])
##
## this result has a 1 in the "1st entry of the b-group" and a -1 in
## the "2nd entry of the u-group"


## here is a textual description of the "equality constraint" matrix.
## We then proceed to implement this description using the function `row` 
## defined above.
##
## day1 clean: b1 - u1 - c1 = 0
## day2 clean: b2 + c1 + f1 - u2 - c2 = 0
## day3 clean: b3 + c2 + s1 + f2 - u3 - c3 = 0
## day4 clean: b4 + c3 + s2 + f3 - u4 - c4 = 0
## day5 clean: b5 + c4 + s3 + f4 - u5 - c5 = 0
## day6 clean: b6 + c5 + s4 + f5 - u6 - c6 = 0
## day7 clean: b7 + c6 + s5 + f6 - u7 = 0

## day1 used:  u1 - s1 - f1  = 0
## day2 used:  u2 - s2 - f2  = 0
## day3 used:  u3 - s3 - f3  = 0
## day4 used:  u4 - s4 - f4  = 0
## day5 used:  u5 - s5 - f5  = 0
## day6 used:  u6 - f6   = 0

## Note that day7 used is a "terminal node" so doesn't have a conservation equation.

## the rc are rows corresponding to conservation laws for "clean" nodes

rc1 = row(b=[(1,1)],c=[(-1,1)],                   u=[(-1,1)])
rc2 = row(b=[(1,2)],c=[(1,1),(-1,2)],          f=[(1,1)],u=[(-1,2)])
rc3 = row(b=[(1,3)],c=[(1,2),(-1,3)],s=[(1,1)],f=[(1,2)],u=[(-1,3)])
rc4 = row(b=[(1,4)],c=[(1,3),(-1,4)],s=[(1,2)],f=[(1,3)],u=[(-1,4)])
rc5 = row(b=[(1,5)],c=[(1,4),(-1,5)],s=[(1,3)],f=[(1,4)],u=[(-1,5)])
rc6 = row(b=[(1,6)],c=[(1,5),(-1,6)],s=[(1,4)],f=[(1,5)],u=[(-1,6)])
rc7 = row(b=[(1,7)],c=[(1,6),(-1,7)],s=[(1,5)],f=[(1,6)],u=[(-1,7)])

## the ru are rows corresponding to conservation laws for "used" nodes

ru1 = row(u=[(1,1)],s=[(-1,1)],f=[(-1,1)])
ru2 = row(u=[(1,2)],s=[(-1,2)],f=[(-1,2)])
ru3 = row(u=[(1,3)],s=[(-1,3)],f=[(-1,3)])
ru4 = row(u=[(1,4)],s=[(-1,4)],f=[(-1,4)])
ru5 = row(u=[(1,5)],s=[(-1,5)],f=[(-1,5)])
ru6 = row(u=[(1,6)],           f=[(-1,6)])

## the rc and ru determined the rows of the matrix defining 

Aeq = np.array([rc1,rc2,rc3,rc4,rc5,rc6,rc7,
                ru1,ru2,ru3,ru4,ru5,ru6])


Alb = np.array([row(u=[(1,i)]) for i in range(1,8)])

## objective function
c = row(b=[(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)],
        f=[(2,1),(2,2),(2,3),(2,4),(2,5),(2,6)],
        s=[(1,1),(1,2),(1,3),(1,4),(1,5)])


tt = np.array([10,10,15,20,40,40,30]) ## these are the ti entries taken from the "tablecloths needed" table


## use linprog to find the point which minimizes the objective function
## we impose equality constraints  Aeq*x=0.
## we also want the inequality constraint Ax >= tt, so we use -Ax <= -tt.
result = linprog(c,A_eq=Aeq,b_eq=np.zeros(13),A_ub=(-1)*Alb,b_ub=(-1)*tt)

def report(result):
    ## the argument ``result`` should be an instance of the class ``scipy.optimize.OptimizeResult`` -- 
    ## i.e. a value of the form returned by ``linprog``
    ##
    x = result.x
    costs = result.fun
    return "\n".join(
        [f"linprog succeeded? {result.success}"]
        +
        [f"Optimal costs on tablecloths for the week are ${costs:.2f}"]
        + 
        ["This is achieved by the following strategy:\n"]
        +
        [f"purchase on day {i+1}: {x[i]:.2f}" for i in range(7)]
        + 
        [""]
        + 
        [f"use on day {i+1}: {x[7+i]:.2f}" for i in range(7)]
        + 
        [""]
        + 
        [f"carry over from day {i+1} to day {i+2}: {x[14+i]:.2f}" for i in range(6)]
        + 
        [""]        
        + 
        [f"to fast laundry on day {i+1}: {x[20+i]:.2f}" for i in range(6)]
        + 
        [""]        
        + 
        [f"to slow laundry on day {i+1}: {x[26+i]:.2f}" for i in range(5)])

print(report(result))
