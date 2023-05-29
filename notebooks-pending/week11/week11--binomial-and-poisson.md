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

Course material (Week 11): Binomial & Poisson distributions
----------------------------------------------------------------
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Intro
=====

Recall that while modeling *Jane's Fish Tank Emporium*, we stipulated that "on average, there is one customer per week" meant that there was a ``1/7`` chance per day of a customer arriving.  With this formulation, there could *never* be 2 customers in a day. On the other hand, that may not be a reasonable assumption.

In this notebook, we are going to talk about more sophisticated probabilistic descriptions.

We'll start by discussing the JFTE example.

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
JFTE, revisited
================

Recall our asusmption is that the probability of a customer visiting the store each day is ``p = 1/7``.

Suppose the store has a 4-hour morning shift and a 4-hour afternoon shift, and suppose that a customer is equally likely to come in the morning shift as in the afternoon shift. 

Then the probability that a customer arrives in the morning shift is $\dfrac{1}{2}\cdot\dfrac{1}{7} = \dfrac{1}{14}$ and similarly the probability that a customer arrives in the afternoon shift is $\dfrac{1}{14}$.

But under this description, it is now possible to have 2 customers arrive in a day. In fact,
the probability of seeing 0, 1 or 2 customers in a day is given by the following table:


| # customers  | probability  |
| :---------:  | ----: |
| 0            | $\dfrac{13 \cdot 13 }{14 \cdot 14}$ |
| 1            | $\dfrac{2 \cdot 13}{14 \cdot 14}$   |
| 2            | $\dfrac{1}{14 \cdot 14}$ |



<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->

Let's compute the *expected value* for the random variable $A$ representing "number of customers arriving in a day":

$$E(A) = 0 \cdot \dfrac{13^2}{14^2}  + 1 \cdot \dfrac{2 \cdot 13}{14 \cdot 14} + 2 \dfrac{1}{14^2} = \dfrac{2}{14} = \dfrac{1}{7}$$

Thus the expected value for the day agrees with the earlier assumption.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
More subdivision
================

Consider instead 4 shifts each of length 2-hours ("early morning", "late morning", "early afternoon", ...) and again suppose that the likelihood of customer arrival is the same for all four shifts. Thus the probability with which a customer arrives during any of the four 2-hour shifts is:

$$p_4 = \dfrac{1}{2}\cdot \dfrac{1}{14} = \dfrac{1}{2^2} \dfrac{1}{7} = \dfrac{1}{28}.$$

With this description, it is now possible to have 4 customers arrive during a day; this will happen
with probabilty

$$(p_4)^4 = \dfrac{1}{28^4}$$



<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->

With what probability do we see 3 customers? Well, this situation will correspond to the arrival of a customer in all but one of the shifts. Now, the probability of having a customer in each shift except (say) the morning shift is

$$p_4^3 \cdot (1-p_4) = \dfrac{1}{28^3} \cdot \left(\dfrac{27}{28}\right)$$

Thus the probability of having exactly 3 customers arrive in a day is

$$4 \cdot (p_4)^3 \cdot (1-p_4)$$
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
The Binomial Theorem
====================

Let $X,Y$ be variables, and let $n \ge 1$ be a whole number. Then

$$(X+Y)^n = X^n + \dbinom{n}{1}X^{n-1}Y + \dbinom{n}{2}X^{n-2}Y^2 + \cdots + \dbinom{n}{n-2} X^2 Y^{n-2} + \dbinom{n}{n-1} X Y^{n-1} + Y^n$$

$$= \sum_{m=0}^n \dbinom{n}{m} X^{n-m} Y^m$$

where the *binomial coefficients* are given by the formula

$$\dbinom{n}{m} = \dfrac{n!}{m!(n-m)!}$$

For example, since $\dbinom{4}{2} = 6$ and $\dbinom{4}{3} = 4$, we have

$$(X+Y)^4 = X^4 + 4 X^3Y  + 6 X^2Y^2 + 4 X Y^3 + Y^4$$
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Return to example:
==================

For $n$ shifts each day, write $p_n = \dfrac{1}{n} \cdot \dfrac{1}{7} = \dfrac{1}{7n}$.

Then the probability that $0 \le m \le n$ customers arrive during the day is given by the product 

$$(\clubsuit) \quad \dbinom{n}{m} (p_n)^m (1-p_n)^{n-m}$$

Indeed, let's represent the outcome symbolically as a list of length $n$, where each member of the list is either the symbol ``1`` or the symbol ``0``.

Thus if $n=5$, the list
$[1,0,0,1,0]$
represents the outcome "a customer arrived in the first and fourth shifts, and no customers arrived in the remaining shifts".


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->

Now, the probability with which a given list $[a_1,a_2,\dots,a_n]$ occurs is $(p_n)^m (1-p_n)^{n-m}$ where
$m$ is the number of indices $i$ for which $a_i = 1$.
And to find the probability that $m$ customers arrive during a given day, one needs to add the probabilities for all such lists' this sum is evidently just the product of the *number* of such lists and the quantity $(p_n)^m (1-p_n)^{n-m}$.

Thus, $(\clubsuit)$ amounts to the assertion that $\dbinom{n}{m}$ is equal to the number of lists $[a_1,a_2,\dots,a_n]$ with $a_i \in \{0,1\}$  for which $m = \#\{i \mid a_i = 1\}$.

**Remark**:
Thus the binomial coefficient $\dbinom{n}{m}$ "counts" the number of ways of choosing $m$ things from a list of $n$ things.

**Remark**:
Think about "FOILing" the expression $(X+Y)^n = (X+Y)(X+Y)^{n-1}$. The coefficient of $X^mY^{n-m}$ in this  expression is a sum of terms
which arise from lists $[a_1,a_2,\dots,a_n]$ as above, where $m = \#\{i \mid a_i = 1\}$. 

E.g. if $n=7$, the list $[0,0,1,1,1,0,1]$ determines the terrm $Y\cdot Y \cdot X \cdot X \cdot X \cdot Y \cdot X = X^4Y^3$.

--------------
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->

Observe that $(\clubsuit)$ together with the binomial Theorem tell us that the probabilities we have found sum to 1:

$$\sum_{m=0}^n \dbinom{n}{m} (p_n)^{n-m} (1-p_n)^m = (1-p_n + p_n)^n = 1^n = 1$$

(use $X = p_n$ and $Y = (1-p_n)$).

Consider the *$Y$-partial derivative* of the expression for $(X+Y)^n$ given by the binomial theorem. One finds that

$$n(X+Y)^{n-1} = \sum_{m=1}^n m\dbinom{n}{m}X^{n-m}Y^{m-1}
=\sum_{m=0}^n m\dbinom{n}{m}X^{n-m}Y^{m-1}$$


so that
$$(\diamondsuit) \quad nY(X+Y)^{n-1} = \sum_{m=0}^n m\dbinom{n}{m}X^{n-m}Y^m$$



<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->


For $n$ shifts in a day, use $(\clubsuit)$ to see that the expected value for the number of customers arriving in a day is given by

$$E(A) = \sum_{i=0}^n i \cdot \dbinom{n}{i} (p_n)^i (1-p_n)^{n-i}$$

Using $(\diamondsuit)$ with $Y = p_n$ and $X = (1-p_n)$, find that

$$E(A) = n \cdot p_n = p_1$$

i.e. in the example $E(A) = \dfrac{1}{7}$ is the "daily probability" we've seen before.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Binomial distribution
=====================

Consider a random variable $B$ representing the outcome of a "binomial experiment" -- thus there are two outcomes: "succeed" and "fail", with "succeed" occuring with probability $0 < p < 1$ and "fail" occuring with probability $1-p$.

Now, we consider $n$ trials of the binomial experiment, and we write $X_n$ for the discrete random variable that represents the number of successes from the $n$ trials.

Just like our "customer arrival" setting, $X_n$ is determined by the binomial distribution. Namely,
the probability $P(X_n=m)$ representing the probability of $m$ successes in $n$ trials
is given by the formula

$$P(X_n = m) = \dbinom{n}{m} p^m (1-p)^{n-m}.$$

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->

A good example of the binomial distribution arises when $B$ is the toss of a fair coin -- so that $p = \dfrac{1}{2}$. In this case, the value of $X_n$ reflects (say) the number of heads in a trial of $n$ coin tosses.

Such a binomial distribution is not *quite* the same as our customer arrival example, though. In our case, the probability of customer arrival depends on the number $n$ of "trials" (or rather, "shifts").

Consider a random variable $B$ describing a binomial outcome as before, where the "success" outcome has probability $0<p<1$. Now consider instead the random variable $Y_n$ which counts the number of successes in  $n$ trials of a binomial experiment
with success probability $\dfrac{p}{n}$. One still often refers to $Y_n$ is a "binomial distribution" --  it satisfies

$$P(Y_n = m) = \dbinom{n}{m} \left(\dfrac{p}{n}\right)^m \left(1-\dfrac{p}{n}\right)^{n-m}.$$

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
A limit of binomial distributions
====================

Let's keep working in the setting of the binomial distribution $Y_n$ just described.

Fix $m$, and consider the probability of $m$ successes in $n$ trials, where we allow $n \to \infty$.

We have
$$P(Y_n = m) = \dbinom{n}{m} \left(\dfrac{p}{n}\right)^m \left(1-\dfrac{p}{n}\right)^{n-m}.$$

Thus
$$(\heartsuit) = \lim_{n \to \infty} P(Y_n = m) = \lim_{n \to \infty} \dbinom{n}{m}\left(\dfrac{p}{n}\right)^m \left(1-\dfrac{p}{n}\right)^{n-m}$$

$$= \lim_{n \to \infty} \dbinom{n}{m}\left(\dfrac{p}{n}\right)^m \left(1-\dfrac{p}{n}\right)^n\left(1-\dfrac{p}{n}\right)^{-m} = A \cdot B \cdot C$$

where

$$A= \lim_{n \to \infty} \dbinom{n}{m} \cdot \left(\dfrac{p}{n}\right)^m 
\quad \text{and} \quad 
B= \lim_{n \to \infty} \left(1-\dfrac{p}{n}\right)^n
\quad \text{and} \quad
C= \lim_{n \to \infty} \left(1-\dfrac{p}{n}\right)^{-m}$$

-------------------------------

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
$$(\heartsuit) = A \cdot B \cdot C \quad \text{where} \quad A= \lim_{n \to \infty}\dbinom{n}{m} \cdot \left(\dfrac{p}{n}\right)^m, \quad
B= \lim_{n \to \infty}\left(1-\dfrac{p}{n}\right)^n, \quad
C= \lim_{n \to \infty}\left(1-\dfrac{p}{n}\right)^{-m}$$


First notice that since $m$  is fixed, we have:

$$\left(1-\dfrac{p}{n}\right)^{-m} \to 1 \quad \text{as $n \to \infty$}$$

so $C=1$.

Now recall that $\left(1 + \dfrac{x}{n}\right)^n \to e^x$ as $n \to \infty$ (calculus!) so that
$B = e^{-p}.$

Finally, 

$$\dbinom{n}{m} \dfrac{p^m}{n^m} = \dfrac{p^m}{m!}\dfrac{n!}{(n-m)!n^m}
= \dfrac{p^m}{m!} \dfrac{n(n-1)\cdots(n-(m-1))}{n^m}$$

$$= \dfrac{p^m}{m!} 1 \cdot \left(1-\dfrac{1}{n}\right)\left(1 - \dfrac{2}{n}\right) \cdots \left(1-\dfrac{m-1}{n}\right)$$

$$\to \dfrac{p^m}{m!}
$$
as $n \to \infty$. 

This shows that $A = \dfrac{p^m}{m!}$ so that the 
$$(\heartsuit) = \dfrac{p^me^{-p}}{m!}.$$ 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Poisson distribution
====================


The limiting distribution described in the previous cell is called the Poisson distribution.
It is a discrete random variable with a countably infinite set of outcomes. More precisely, the Poisson distribution describes a random variable $X_{\operatorname{poisson}}$ whose
outcomes are $m=0,1,2,\dots$ and for which 

$$P(X_{\operatorname{poisson}} = m) =  \dfrac{p^me^{-p}}{m!}$$

for $m = 0,1,2,\cdots$.

Now, if this is really a probability distribution, it should be the case that

$$\sum_{m \ge 0} P(X_{\operatorname{poisson}} = m) = 1$$.

Well,

$$\sum_{m \ge 0} P(X_{\operatorname{poisson}} = m) = \sum_{m \ge 0} \dfrac{p^me^{-p}}{m!} = 
e^{-p} \sum_{m \ge 0} \dfrac{p^m}{m!} = e^{-p} e^p = 1.$$
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->

Let's compute the *expected value* $E(X_{\operatorname{poisson}})$. Well,

$$E(X_{\operatorname{poisson}}) = \sum_{m \ge 0} m \cdot P(X_{\operatorname{poisson}} = m)$$

$$ = \sum_{m \ge 0} m \dfrac{p^m e^{-p}}{m!} = pe^pe^{-p} = p.$$


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Return to JFTE
==============

We may use the Poisson distribution to model customer arrival $X$ -- thus the probability that
$m$ customers arrive over the course of 1 day is given by

$$P(X = m) = \dfrac{p^m\cdot e^{-p}}{m!}$$

where $p = \dfrac{1}{7}$.

Remarks:
=======

- Poisson distributions are important in queuing theory and other areas, as they describe prob-
abilities of independent events, such as the arrival of customers.

- The first practical application was due to Ladislaus Bortkiewicz. In 1898, he investigated
the number of soldiers in the Prussian army who died each year from being kicked by a horse. Poisson distributions are ideal for modeling events that have a really low probability of occurring, but many opportunities to occur.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Implementation
===============

How can we use the Poisson distribution in practice? e.g. with our JFTE simulation??

Let's compute the probabilities for $m = 0,1,2,...$ for customer arrival, as before:

<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
import numpy as np

def poisson(p,m):
    return (1.*p**m/ np.math.factorial(m))*np.exp(-p)

print("\n".join([f"m = {m} -- q_{m+1} = P(X={m}) = {poisson(1./7,m):.8f}" for m in range(6)]))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Addendum
========

We want to simulate arrival of customers according to the Poisson distribution. 
In fact, we only approximate this, because while the Poisson distribution allows for any number of customers, our simulation is going to impose an upper bound on the number.

So: we desire a ``python`` function which takes as arguments ``p`` the base probability of an event and ``M`` the maximum number of  events to consider.

In our case we are modeling customer arrivals, so we'll call this function ``arrival``. Our function will compute the first ``M-1`` probabilities ``q0,q1,...,q{M-1}`` for the Poisson distribution.
We then set ``qM`` to be ``1 - q0 - q1 - ...``

```
def arrival(p=1./7,M = 10,rng=default_rng()):
    qq = list(map(lambda m:poisson(p,m),range(M)))
    qq = qq + [1-sum(qq,0)]
    
    return rng.choose(range(M+1),p=qq)
```
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
from numpy.random import default_rng
rng=default_rng()

def arrival(p=1./7,M = 10,rng=default_rng()):
    qq = list(map(lambda m:poisson(p,m),range(M)))
    qq = qq + [1-sum(qq,0)]
    
    return rng.choice(list(range(M+1)),p=qq)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Another construction
====================

*Originally, I used the following alternative construction for the function ``arrival``. It is slightly more complicated, but I'll leave it here for reference.*

We now consider the consecutive intervals

$$I_0=[0=q_0,q_1), \quad I_1=[q_1,q_1+q_2), \quad I_2=[q_1+q_2,q_1+q_2+q_3), \quad 
\cdots$$

We simulate a value of $X$ by choosing a  random number $0 < r < 1$; we then find the value of $m$ such that
$r \in I_m$ and we set $X=m$.

Thus $X=m$ if and only if $$\sum_{i=1}^m q_i \le r < \sum_{i=1}^{m+1} q_i$$

We'll write a ``python`` function which takes as parameter the base probability $p$, and a specified "maximum number of customers" ``N``. The function computes $q_0,q_1,\cdots,q_N$,
gets a random real number $r$ in $[0,1]$ and determines which subinterval $I_m$ contains $r$,
where for $m<N$ the interval $I_m$ is as before, and where the $N$th subinterval is defined to be $$I_N = \left[\sum_{i=1}^N q_i,1\right].$$
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
from numpy.random import default_rng

rng=default_rng()

def partial_sum(l,i):
    return sum(l[0:i],0)

def arrival_alt(p=1.7,M=10,rng=default_rng()):
    ## make a list of the values q_i 
    qq = list(map(lambda m:poisson(p,m),range(M+1)))
    
    ## find the "partial sums" of the list qq
    pq = list(map(lambda m:partial_sum(qq,m),range(M+1)))
    
    r = rng.random()
    
    for i in range(M):
        if r < pq[i+1]:
            return i
    else:
        return M
    
```

<!-- #region slideshow={"slide_type": "subslide"} -->
-------------------------

The function ``arrival`` *(or ``arrival_alt``)* just introduced makes it possible to simulate customer arrival using the Poisson distribution.

For example, to create a list containing a simulation of 6 months worth of customer arrival data with probability ``p=1/7``, allowing no more than 10 customers per day, proceed as follows:

```
customers = [arrival(p=1./7,M=10) for n in range(6*4*7)]
```

or equivalently
```
customers = []
for n in range(6*4*7):
  customers.append(arrival(p=1./7,M=10))
```

<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
customers_1 = [arrival(p=1./7,M=10) for n in range(6*4*7)]

customers_2 = []
for n in range(6*4*7):
  customers_2.append(arrival(p=1./7,M=10))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
If you inspect the lists ``customers_1`` or ``customers_2`` from the preceding cell, you should
see that the lists mainly -- perhaps even exclusively -- contain the entries ``0`` and ``1``.

To make larger numbers of customer arrivals likely to appear in our arrival data, we need to wait longer!!

Let's use a ``pandas`` DataFrame to keep track of the frequency of customer counts:
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
import pandas as pd

def get_customers(p,N):
    return [arrival(p,10) for n in range(N)]

year = 52*7

data = pd.DataFrame(get_customers(1./7,10*year))
data.value_counts()
```

```python slideshow={"slide_type": "fragment"}
## values for 100 years
pd.DataFrame(get_customers(1./7,100*year)).value_counts()
```

```python slideshow={"slide_type": "fragment"}
## values for 1,000 years
pd.DataFrame(get_customers(1./7,1000*year)).value_counts()
```

```python

```
