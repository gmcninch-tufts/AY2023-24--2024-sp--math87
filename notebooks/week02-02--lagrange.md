---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  nbformat: 4
  nbformat_minor: 5
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  language_info:
     codemirror_mode:
       name: ipython
       version: 2
     file_extension: ".py"
     mimetype: "text/x-python"
     name: "python"
     nbconvert_exporter: "python"
     pygments_lexer: "ipython2"
     version: "2.7.15"
---

::: {.cell .title}
# [George McNinch](http://gmcninch.math.tufts.edu) Math 87 - Spring 2024

# Week 2 
# § Lagrange multipliers
:::

::: {.cell}

# Some motivation

Let's recall our television manufacturing example for a moment. The
model we solved was interesting but most likely unrealistic. A
manufacturer, for instance, probably has a limited capacity and can
only produce a certain amount of TVs in total per year.

Let’s look at an example where that capacity is 10,000 TVs per year.

So given the *constraint*, $s + t ≤ 10,000$, how many of each model
should they produce now??

Well, first notice that the *unconstrained optimum* ofwith $s = 4,735$
and $t = 7,043$, does not satisfy the constraint.

Now let's recall that in the single variable case, trying to find a
*constrained optimum* amounts t optimizing a function on a closed
interval -- so you proceed with the usual procedure for optimization
but must also check boundary points (endpoints).

If we proceed in this fashion, we'd check the "boundary" conditions
corresponding to $t=0$ and $s=0$.

Well, setting $t=0$ we see that the profit function is given by

$$P(s,0) = 144s - 0.01s^2 - 400,000.$$

Since this is a function only of $s$ we can use 1-dimensional
optimization techniques:

$$\dfrac{\partial P}{\partial S}(S,0) = 144 - 0.02s = 0 \implies s = 7,200.$$

On this boundary, we need to consider $(0,0)$ and $(10,000,0)$ (the
boundary of the boundary...) as well as $(7,200,0)$.

We can treat the boundary with $s =0$ similarly.

But the boundary condition with $s+t = 0$ will be more of a pain.

The method of Lagrange multipliers gives a more systematic way to
proceed!

:::


::: {.cell}

# Lagrange multipliers

Consider a function $f(x,y)$ of two variables. We are interested here
in finding maximal or minimal values of $f$ subject to a
*constraint*. The sort of constraint we have in mind is a restriction
on the possible pairs $(x,y)$ -- so we have a second function $g(x,y)$
and we want to maximize (or minimize) $f$ subject to the condition
that $g(x,y) = c$ for some fixed quantity $c$.

We introduce a "new" function -- now of *three* variables - known as
the **Lagrangian**. It is given by the formula $$F(x,y,\lambda) =
f(x,y) - \lambda \cdot (c-g(x,y))$$

(We use the Greek letter $\lambda$ for our third variable in part
because it plays a different role for us than the variables $x,y$).

We can calculate the *partial derivatives* of this Lagrangian; they
are:

$$\dfrac{\partial F}{\partial x} = \dfrac{\partial f}{\partial x} -
\lambda\dfrac{\partial g}{\partial x}$$

$$\dfrac{\partial F}{\partial y} = \dfrac{\partial f}{\partial y} -
\lambda\dfrac{\partial g}{\partial y}$$

$$\dfrac{\partial F}{\partial \lambda} = c-g(x,y)$$

If we seek critical points of the Lagrangian, we find that

$$0 = \dfrac{\partial F}{\partial x} = \dfrac{\partial f}{\partial
x} - \lambda\dfrac{\partial g}{\partial x}$$

and similarly for $y$, so that

$$ \dfrac{\partial f}{\partial x} = \lambda \dfrac{\partial
g}{\partial x} \quad \text{and}\quad \dfrac{\partial f}{\partial y} =
\lambda \dfrac{\partial g}{\partial y}$$ 

i.e.  $$ \left (\dfrac{\partial f}{\partial x} \mathbf{i} +
\dfrac{\partial f}{\partial y} \mathbf{j} \right) = \lambda \left
(\dfrac{\partial g}{\partial x} \mathbf{i} + \dfrac{\partial
g}{\partial y} \mathbf{j} \right)$$

(Recall that $\dfrac{\partial f}{\partial x} \mathbf{i} +
\dfrac{\partial f}{\partial y} \mathbf{j}$ is the *gradient* $\nabla
f$ of $f$).

Moreover, we find that $$0 = \dfrac{\partial F}{\partial \lambda} =
c - g(x,y).$$

Summarizing, the condition that $(x_0,y_0,\lambda_0)$ is a critical
point of $F$ is equivalent to two requirements:

- **(A)** $(x_0,y_0)$ must be on the level curve $g(x,y) = c$, and
- **(B)** the gradient vectors must satisfy $\nabla f
  \vert_{(x_0,y_0)} = \lambda_0 \nabla g \vert_{(x_0,y_0)}$.

## The crucial assertion is this:


> Optimal values for $f$ along the level curve $g(x,y) = c$ will be
> found among the critical points of $F$.

Indeed, suppose $(x_0,y_0)$ is a point on the level curve at which $f$
takes its max (or min) value (on the level surface).  We need to argue
that the gradient vector $\nabla f \vert_{(x_0,y_0)}$ is "parallel" to
the gradient vector $\nabla g \vert_{(x_0,y_0)}$ -- i.e. **(B)** above
holds.

More precisely, we can write $\nabla f \vert_{(x_0,y_0)} =
\mathbf{v} + \mu \nabla g \vert_{(x_0,y_0)}$ for a vector $\mathbf{v}$
perpendicular to $\nabla g \vert_{(x_0,y_0)}$ (and for some scalar
$\mu$).  And we must argue that $\mathbf{v}$ is zero.

But if $\mathbf{v}$ is non-zero, then walking along the level curve
$g(x,y) = c$ "in the direction of $\mathbf{v}$" will lead to higher
values of $f$, contrary to the assumption that on the level curve, $f$
has a maximum at $(x_0,y_0)$.  $\quad \blacksquare$

:::

::: {.cell}

# Televisions, again


Let’s return to the television manufacturing problem. We consider the
constraint $$g(s, t) = s + t = 10,000$$ i.e. "the manufacturer
produces exactly 10,000 televisions".

Consider the *Lagrangian* function $F(s,t,\lambda) = P(s,t) -
\lambda(s+t-10,000).$

Looking for critical points of $F$, we find that:

$$ \left \{ \begin{matrix} \dfrac{\partial P}{\partial s} - \lambda
\dfrac{\partial g}{\partial s} &=& 144 − 0.02s − 0.007t − λ &= 0 \\
\dfrac{\partial P}{\partial t} - \lambda \dfrac{\partial g}{\partial
t} &=& 174 − 0.007s − 0.002t − λ &= 0 \\ g(s,t) - c &=& -10000 +s +t
&= 0 \end{matrix} \right .$$

This leads to 3 linear equations in 3 unknowns, which we can easily
solve with ``numpy`` (or by hand!):
:::

::: {.cell .code}
```python
import numpy as np

## coefficient matrix
M=np.array([[0.02,.007,1],[.007,.02,1],[1,1,0]])

b=np.array([144,174,10000])

np.linalg.solve(M,b)
```
:::

::: {.cell} 

We find that $s \approx 3,846$, $t \approx 6,154$ and $λ = 24$.  

:::


::: {.cell} 

Now, effectively we consider the profit function $P$
subject to the constraint $s+t=10,000$ where $s \ge 0$ and $t \ge
0$. On this "closed interval", the function $P$ will assume a maximum
and a minimum value. We've found the "critical point" of $P$ on this
"interval" -- namley $(3846, 6154)$. The *endpoints* of the interval
are $(0,10000)$ and $(10000,0)$.


Let's compare the values of $P$ at these points of interest:

:::

::: {.cell .code}
```python
def p(s,t):
    return -400000 + 144*s + 174*t - 0.01*s**2 - 0.01*t**2 - .007*s*t

[p(0,10000), p(3846,6154), p(10000,0)]
```
:::

::: {.cell}

This shows that the *maximum constrained profit* is $$P(3846 , 6154) =
532308.$$

(what choice of $s,t$ give the minimum constrained profit? Could you
have guessed that *a priori*?)
:::

::: {.cell}
# Shadow prices and an interpretation for the "multiplier" $\lambda$


Let's carry out *sensitivity analysis* on the value of the
*constraint*.

Recall that our constraint is $g(s,t) = s+t = 10000$. So we instead
set $$g(s,t) = s + t = c.$$

In this case, we must instead solve the system of equations $Mx = b$
where $$M = \begin{pmatrix} 0.02 & 0.007 & 1 \\ 0.007 & 0.02 & 1 \\ 1
& 1 & 0 \end{pmatrix} \quad \text{and} \quad b = \begin{pmatrix} 144
\\ 174 \\ c \end{pmatrix}$$


Since the vector $b$ has an "unknown", we can't seem to use the
``linalg.solve`` method. We can circumvent this by inverting the
coefficient matrix. We must also introduce a ``symbol`` for the
unknown ``c``.  
:::

::: {.cell .code}
```python
import numpy as np
import sympy as sp

## coefficient matrix
M=np.array([[0.02,0.007,1],[0.007,0.02,1],[1,1,0]])

## inverse of coefficient matrix
Mi = np.linalg.inv(M)

c = sp.Symbol('c')
b=np.array([144,174,c])


np.matmul(Mi,b)

```
:::

::: {.cell}

So we see that the solution has $$s = \dfrac{c}{2} - 1153.85 \qquad t
= \dfrac{c}{2} + 1153.85 \qquad \text{and} \qquad \lambda = 159
- 0.0135c.$$

Thus $\dfrac{ds}{dc} = \dfrac{dt}{dc} = \dfrac{1}{2}$ so that
$$S(s,c=10000) \approx 1.3 \quad S(t,c=10000) \approx 0.8$$ which
shows that increasing the maximum production of TVs will increase the
optimal production levels.

What about the sensitivity $S(P,c) = \dfrac{dP}{dc} \cdot
\dfrac{c}{P}$?

To compute $\dfrac{dP}{dc}$ we can use the several-variable chain
rule, or just rewrite $P$ as a function of $c$. After some
calculation, we find that $$S(P,c=10000) \approx 24 \cdot
\dfrac{10000}{532308} \approx 0.45.$$ So a 1% increase in $c$ yields a
$0.45%$ increase in $P$.

Interestingly, observe that $$\dfrac{dP}{dc} = \lambda.$$

Let's pause to recall that with the method of Lagrange multipliers,
the value of gradient of the function we are optimizing -- $P$ in this
case -- at a candidate optimal point is proportional to the value of
the gradient of $g$: $$ \nabla(P)_{(s_0,t_0)} = \lambda
\nabla(g)_{(s_0,t_0)}$$

One refers to $\dfrac{\partial P}{\partial c}$ as the **shadow price**
-- increasing $c$ by 1 unit in this case increases $P$ by about \$24.

Thus, the Lagrange multiplier, λ actually has a "physical" meaning
here. If you are allowed to produce more TV’s it tells you how much
that change affects your profit. Therefore, if the cost of making that
change is less than the additional profit, you probably should go for
it!

:::
