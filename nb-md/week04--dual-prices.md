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

Course material (Week 4): Dual prices & integer programming
-----------------------------------------------------------


Recollections
=============

Let's briefly recall the notion of *slack variables* and *complementary slackness* from our duality discussion.

To this end, consider a linear program $\mathcal{L}$ given by
$(\mathbf{c} \in \mathbb{R}^{1 \times n},A \in \mathbb{R}^{r \times n}, \mathbf{b} \in \mathbb{R}^r)$ which seeks to ``maximize`` its objective function. We write $\mathbf{0} \le \mathbf{x} \in \mathbb{R}^n$ for the variable vector of our linear program, and we recall that it satisfies $A \mathbf{x} \le \mathbf{b}$.

As usual we'll write $\mathcal{L}'$ for the dual linear program -- it is determined by the triple $(\mathbf{b}^T,A^T,\mathcal{c}^T)$; it seeks to ``minimize`` its objective function; the dual varible vector is written
$\mathbf{y} \in \mathbf{R}^r$ and it satisfies $\mathbf{y} \ge \mathbf{0}$ and
$A^T\mathbf{y} \ge \mathbf{c}^T$.

*Complementary slackness* is the assertion that for feasible points $\mathbf{x}$ for $\mathcal{L}$ and $\mathbf{y}$ for $\mathcal{L}'$, $\mathbf{x}$ is optimal for $\mathcal{L}$ and $\mathbf{y}$ is optimal for $\mathcal{L}'$ if and only if

$$(\clubsuit) \quad (\mathbf{b} - A\mathbf{x})^T \cdot \mathbf{y} = 0 \quad \text{and} \quad (\mathbf{y}^TA - \mathbf{c}) \cdot \mathbf{x} = 0.$$

For optimal vectors $\mathbf{x}^*$ and $\mathbf{y}^*$ we refer to the slack vectors:

$$(\mathbf{b} - A\mathbf{x}^*) \quad \text{and} \quad ((\mathbf{y}^*)^TA - \mathbf{c})$$

**Remark**: Recall that if $\mathbf{x}$ is a feasible point for $\mathcal{L}$, then $A \mathbf{x} \le \mathbf{b}$ or put another way, the slack vector $\mathbf{b} - A\mathbf{x} \ge \mathbf{0}$ is non-negative. Now, if also $\mathbf{y} \ge \mathbf{0}$, it is easy to see that the product -- a scalar quantity -- satisfies

$$(\mathbf{b} - A\mathbf{x})^T\cdot \mathbf{y} \ge 0$$ 

and that in order to have $(\mathbf{b} - A\mathbf{x})^T\cdot \mathbf{y} = 0$ for a non-zero vector $\mathbf{y}$, some of the coefficients of $\mathbf{b} - A\mathbf{x}$ must be zero; in the discussion below we say that those coefficients - or the corresponding constraints -- are *binding*.


Example 
=======

A company has acquired 100 lots on which to build homes of two styles: Cape Cod and Ranch. They will build these homes over a year, during which they will have available
13,000 hours of bricklayer labor and 12,000 hours of carpenter labor. Each Cape Cod house requires
200 hours of carpentry labor and 50 hours of bricklayer labor. Each Ranch house requires 120 hours
of bricklayer labor and 100 hours of carpentry. The profit for building a Cape Cod home is projected
to be \\$5,100 and each Ranch home is projected to be \\$5,000.
How many of each type of house would you recommend building?

Variables: 

- $C$ = # Cape Cod homes built
- $R$ = # Ranch homes built

Primal linear program: *maximize* for the data $(\mathbf{c},A,\mathbf{b})$.

- $\mathbf{c} = \begin{bmatrix} 5100 & 5000 \end{bmatrix}$
- $A = \begin{bmatrix} 1& 1 \\  200 & 100 \\ 50 & 120 \end{bmatrix}$
- $\mathbf{b} = \begin{bmatrix} 100 \\ 12000 \\ 13000 \end{bmatrix}$

i.e. the objective function is given by $\mathbf{c} \cdot \begin{bmatrix} C \\ R \end{bmatrix} = 5100C + 5000R$ where $\begin{bmatrix} C \\ R \end{bmatrix} \ge \mathbf{0}$.

And $A \cdot \begin{bmatrix} C \\ R \end{bmatrix} \le \mathbf{b}$.

-----

Thus the dual linear program is given by the data $(\mathbf{b}^T,A^T,\mathbf{c}^T)$.

We label the variables of the dual linear program using the two resource constraints: $\mathbf{y} = \begin{bmatrix}
y_l \\ y_c \\ y_b
\end{bmatrix}$ where $y_l$ denotes the unit price of a lot, $y_c$ denotes the unit price of carpentry labor, and $y_b$ denotes the unit price of bricklayer labor.

So the objective function for the dual system is given by
$$\mathbf{b}^T \cdot \begin{bmatrix}
y_l \\ y_b \\ y_c
\end{bmatrix} = 100y_l + 12000y_b + 13000y_c$$ 
and the inequality constraints are given by
$$A^T \cdot  \begin{bmatrix}
y_l \\ y_b \\ y_c
\end{bmatrix} \ge \mathbf{c}^T = \begin{bmatrix} 5100 \\ 5000 \end{bmatrix}$$

```python
from scipy.optimize import linprog
import numpy as np

c = np.array([5100,5000])
A = np.array([[1,1],[200,100],[50,120]])
b = np.array([100,12000,13000])

primal = linprog((-1)*c,A_ub = A,b_ub = b)

dual = linprog(b,A_ub = (-1)*A.T,b_ub = (-1)*c)

print("** primal:\n",primal,"\n\n-----------\n\n")
print("** dual:\n",dual)
```

So ``scipy`` confirms that an optimal solution  to the primal linear system is

$$\mathbf{x}^* = \begin{bmatrix} C \\ R \end{bmatrix} = \begin{bmatrix} 20 \\ 80 \end{bmatrix}$$

Note that $\mathbf{c} \cdot \begin{bmatrix} 20 \\ 80 \end{bmatrix} = \$502,000$

And an optimal solution to the dual linear system is

$$\mathbf{y}^* = \begin{bmatrix} y_l \\ y_b \\ y_c \end{bmatrix} = \begin{bmatrix} 4900 \\ 1 \\0\end{bmatrix}$$

------

Let's try to understand what the *slack vectors* are telling us.

Let's compute
$$(\mathbf{b} - A\mathbf{x}^*) \quad \text{and} \quad ((\mathbf{y}^*)^TA - \mathbf{c})$$


```python
xstar = primal.x    # we get the vector from the .x member of the 
                    # class returned by linprog
    
ystar = dual.x

slack_primal = b - A@xstar
slack_dual = ystar@A - c

print(slack_primal)
print(slack_dual)

```

We focus on 
$$(\mathbf{b} - A\mathbf{x}^*) \approx \begin{bmatrix} 0 \\ 0 \\ 2400 \end{bmatrix}$$

First, this confirms (at least part of) the complementary slackness result; indeed,
$$(\mathbf{b} - A\mathbf{x}^*)^T \cdot \mathbf{y}^* =  \begin{bmatrix}
0 & 0 & 2400\end{bmatrix} \cdot \begin{bmatrix} 4900 \\ 1 \\0\end{bmatrix} = 0.$$

In general, *one says that the constraints -- or the dual variables -- corresponding to zero entries of the slack vector are binding*. 

In this case, the first and second entries of the slack variable $\mathbf{b} - A\mathbf{x}^*$ are zero, and hence the "lots" and "carpentry" constraints are binding; the resulting dual prices are 4900 for lots and 1 for carpentry.
But we have an oversupply of available bricklaying, and thus the dual price for bricklaying is 0.

As some heuristic evidence for why we see the result we do, note that Cape Cod houses are more profitable, but require more carpentry.

Understanding the dual prices
=============================
Let's try to understand the meanining of the dual prices in this case.
The *dual price lemma* -- see the slide below -- shows that -- roughly speaking -- the dual price
predicts the change in the objective function if the right-hand side of the constraint inequality changes by 1.

Imagine that the owner of 15 lots adjacent to the development describe above offers to sell them for \\$60,000 total. Should you buy them?

Well, this amounts to changing the inequality $C+R \le 100$ to $C+R \le 115$.
Since the dual price of lots is \\$4900, we predict a gain in profit of
\\$ $4900 \times 15$. For total price \\$60,000 for the 15 lots amounts to a per-lot price of \\$4000 per lot.

So, if the prediction is correct, we would make a profit of \\$900 per lot!

Re-reading the fine print on the lemma below, however, we actually see that it isn't quite true "on the nose" that changes in the constraint values cause the objective function to increases by the corresponding multiple of the dual price -- in fact, that increase is only an "upper bound" (however, see the remark below the lemma for some justification for why it is not an unreasonable estimate to use).

In fact, re-running the linear program after replacing the inequality constraint by $C+R \le 115$, 
our profits increase from \\$502,000 to \\$563,895
i.e. by roughly \\$62,000. After we spend the \\$60,000 on the new lots,
we only net \\$2,000. So we make considerably less than the estimated 
\\$ $900 \times 15 = 13,500$.






```python
bprime = b + np.array([15,0,0])

primal_tweaked = linprog((-1)*c,A_ub = A,b_ub = bprime)

dual_tweaked   = linprog(bprime,A_ub = (-1)*A.T,b_ub = (-1)*c)

[primal_tweaked.x, primal_tweaked.fun, primal_tweaked.slack, dual_tweaked.x]
```

As a final comment, one can recompute the slack vector for the "new" linear program (with $C+R \le 115$) - one now finds no slack at all in either of the labor contraints (so they are both *binding*), but there is now slack in the *lot* constraint, which reflects an "oversupply" of lots.

```python

```

<!-- #region -->
Dual price lemma
----------------

Let's consider again a linear program $\mathcal{L}$ in standard form given by data $(\mathbf{c},A,\mathbf{b})$.

Let $\Delta \mathbf{b} \in \mathbb{R}^r$ be a small perturbation of $\mathbf{b} \in \mathbb{R}^r$.

**Lemma:** Suppose that $\mathbf{x}^*$ is an optimal solution to the linear program $\mathcal{L}$ and that $\mathbf{x}'$ is an optimal solution to the linear program
$\mathcal{L}_\Delta$ given by the data $(\mathbf{c},A,\mathbf{b} + \Delta \mathbf{b})$.
Then 

$$\mathbf{c} \cdot \mathbf{x'} \le \mathbf{c} \cdot \mathbf{x}^* + \Delta \mathbf{b}^T \cdot \mathbf{y}^*$$

where $\mathbf{y}^*$ is an optimal solution to the dual linear system $\mathcal{L}'$.


**Remark** One can actually prove equality in the lemma provided that
the perturbation $\Delta \mathbf{b}$ vector is "small enough".

**Proof of Lemma:**

Note that the constraints of the unaltered dual $\mathcal{L}'$ are the same as those of the altered dual $\mathcal{L}_a'$. Thus, an optimal solution $\mathbf{y}^*$ for $\mathcal{L}'$ is at least feasible for $\mathcal{L}_a'$.

So we may apply the weak duality theorem to see that

$$(*) \quad \mathbf{c} \cdot \mathbf{x}' \le (\mathbf{b} + \Delta \mathbf{b})^T \cdot \mathbf{y}^*
= \mathbf{b}^T \cdot \mathbf{y}^* + \Delta \mathbf{b}^T \cdot \mathbf{y}^*.$$

However, by strong duality of the unaltered linear programs, we have
$$\mathbf{c} \cdot \mathbf{x}^* = \mathbf{b}^T \cdot \mathbf{y}^*;$$
substituting in $(*)$ we find
$$ \mathbf{c} \cdot \mathbf{x}' \le \mathbf{c} \cdot \mathbf{x}^* + \Delta \mathbf{b}^T \cdot \mathbf{y}^*$$ 
as required.
**QED**
<!-- #endregion -->

```python

```
