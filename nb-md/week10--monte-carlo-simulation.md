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

<!-- #region slideshow={"slide_type": "slide"} -->
Math087 - Mathematical Modeling
===============================
[Tufts University](http://www.tufts.edu) -- [Department of Math](http://math.tufts.edu)  
[George McNinch](http://gmcninch.math.tufts.edu) <george.mcninch@tufts.edu>  
*Fall 2020*

Course material (Week 10): Monte-Carlo simulation
----------------------------------------------------------------
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
A modeling application of Monte-Carlo methods: fish tanks!
==========================================================

In this notebook we are going to discuss a modeling example.

Suppose that you have been promoted to inventory manager at **Jane's Fish Tank Emporium** (JFTE).

JFTE sells only 150 gallon fish tanks that are bulky, so it prefers to not keep more in stock than are needed at any given point in time.

Suppose that on average JFTE sells one tank per week. 

JFTE can order new tanks at any point, but they must wait 5 days for the arrival of a new tank once it has been ordered.

The task is to design a good strategy for ordering fish tanks.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Relevant questions & parameters??
============

- profit from the sale of a tank?
- cost of storage for an unsold tank in stock?
- what does "on average, one tank is sold per week" really mean??
- what strategies are even possible?

Let's consider some extremal cases first:

- if the profit per tank is large and the storage costs for an in-stock tank relatively small, then a good strategy is to keep a relatively large inventory.
- if the profit per tank is small and the storage costs for an in-stock tank are relatively large, then a good strategy is to keep little-or-no inventory and order as required.

It is difficult to formulate too many generalities without knowing further information.

An important rule of modeling we'd like to follow is this:

Start with a relatively simple model, but build it to allow incremental additions of complexity.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Simplifying assumptions
=======================

1. Let's assume that "on average, JFTE sells one tank per week" means that on any given day, there is a 
$\dfrac{1}{7}$ chance of an interested customer entering the store.

2. If an interested customer arrives but there is no stock, the potential sale is then *lost* (thus our model doesn't acknowledge rainchecks or instructions to a customer to "try next week").

3. The cost of storing a tank is high enough that you only want to store tanks you expect to sell "soon".

These assumptions suggest two strategies, which we want to compare.

**Strategy A.** Set a *standing order* to have one tank delivered each week.  
**Strategy B.** Order a new tank whenever one is sold -- *on-demand ordering*

We are going to use a Monte-Carlo simulation to compare these two strategies.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Our simulation
==============

The first step is to simulate arrival of customers. We are going to make a list of $N$ days for our simulation, and for each day we are going to use a random selection to "decide" whether a customer arrives.

For each day, we would like to keep track of various information:

- does a customer arrive? (determined randomly)
- is there a tank in stock? (ordering is determined by our strategy)

So let's create a ``python`` data structure which keeps track of the required information. We'll just use a ``class`` named ``JFTE`` which has instance variables ``customers``, ``stock``, ``sales`` etc.
  
When we construct an instance of the class, we indicate the number of days ``N`` for our simulation. We create a list corresponding to ``days``, and the random number generated "decides" whether or not a customer will arrive on the given day.

We now implement our *strategies* as functions which take as argument an instance of the class ``JFTE``
and return an instance of the class ``result``.


<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
import numpy as np
import itertools as it

from numpy.random import default_rng
rng = default_rng()

```

```python slideshow={"slide_type": "subslide"}

def customer(prob=1./7):
    return rng.choice([1,0],p=[prob,1-prob])


class JFTE():
    def __init__(self,N,prob=1./7):
        self.customers = [customer() for n in range(N)]
        self.reset()
    
    def reset(self):
        self.stock = 1
        self.sales = 0
        self.lost_sales = 0
        self.storage_days = 0
        self.max_stock = 1
    
    def num_days(self):
        return len(self.customers)
    
    def add_stock(self):
        self.stock = self.stock + 1
        if self.stock > self.max_stock:
            self.max_stock = self.stock
    
    def sale(self):
        self.stock = self.stock - 1
        self.sales = self.sales + 1
        
    def result(self):
        return result(self.num_days(),self.sales,self.lost_sales,
                      self.storage_days,self.max_stock)

```

```python slideshow={"slide_type": "subslide"}
class result():
    def __init__(self,num_days,sales,lost_sales,storage_days,max_stock):
        self.num_days = num_days
        self.sales = sales
        self.lost_sales = lost_sales
        self.storage_days = storage_days
        self.max_stock = max_stock

    def report(self):
        entries = [f"weeks:        {self.num_days/7.}",
                   f"sales:        {self.sales}",
                   f"lost sales:   {self.lost_sales}",
                   f"storage_days: {self.storage_days}  (effective)",
                   f"max stock:    {self.max_stock}",
                    ]
        return "\n".join(entries)
        
```

<!-- #region slideshow={"slide_type": "slide"} -->
The first strategy is to have a standing order made each week on the same day.

<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
def stand_order(J,dow=6):
    ## dow = arrival day-of-week for standing order; should be in [0,1,2,3,4,5,6]
    ## we'll assume that the first day of the ``days`` list is dow=0.
    
    N = J.num_days()
    J.reset()
    
    for i in range(N):
        c = J.customers[i]
        if dow == np.mod(i,7):
            J.add_stock()
        if c>0 and J.stock == 0:
            J.lost_sales = J.lost_sales + 1
        if c>0 and J.stock > 0:
            J.sale()
        J.storage_days = J.storage_days + J.stock
    return J.result()

```

<!-- #region slideshow={"slide_type": "slide"} -->
The second strategy is to have a order placed as soon as a sale is made.
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
def order_on_demand(J):
    J.reset()
    order_wait = np.inf
    for c in J.customers:
        if c>0 and J.stock==0:
            J.lost_sales = J.lost_sales + 1
        if c>0 and J.stock>0:
            J.sale()
            
        J.storage_days = J.storage_days + J.stock
        if  order_wait == np.inf and J.stock==0:
            order_wait = 5
        if order_wait == 0:
            J.add_stock()
            order_wait = np.inf
        if order_wait>0:
            order_wait = order_wait - 1
    return J.result()

```

```python slideshow={"slide_type": "slide"}
J = JFTE(2*52*7)

J1 = stand_order(J,dow=6)
J2 = order_on_demand(J)

```

```python slideshow={"slide_type": "fragment"}
print(J1.report())
```

```python slideshow={"slide_type": "fragment"}
print(J2.report())
```

```python slideshow={"slide_type": "slide"}
import pandas as pd

JL = list(map(JFTE,10*[2*52*7]))

def report_trials(JL):
    JS = list(map(stand_order,JL))
    JD = list(map(order_on_demand,JL))
    rdict = {"sales       - standing":list(map(lambda x:x.sales,     JS)),
             "lost sales  - standing":list(map(lambda x:x.lost_sales,JS)),
             "storage_days- standing":list(map(lambda x:x.storage_days,JS)),
             "max stock   - standing":list(map(lambda x:x.max_stock,JS)),
             "sales       - demand":  list(map(lambda x:x.sales,     JD)),
             "lost sales  - demand":  list(map(lambda x:x.lost_sales,JD)),
             "storage_days- demand":  list(map(lambda x:x.storage_days,JD)),
             "max stock   - demand":list(map(lambda x:x.max_stock,JD))
              }
    return pd.DataFrame(rdict)
```

```python slideshow={"slide_type": "subslide"}
report_trials(JL)
```


