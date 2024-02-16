---
title: Midterm Project 1 -- Supply chain *solutions*
author: George McNinch
date: due 2024-02-16
---

# Instructions

Complete the project report described below in the style of a lab
report. You may attach embedded code in the
submitted PDF. Take care to explain fully the formulation of linear
programs and the associated flow diagrams -- including all choices of
nodes and edges. Write a summary of your solution, identifying the
optimal shipping routes and how to deal with unexpected crises.

# The problem


In this problem, consider yourself to be the logistics manager for a
supply-chain company that makes and sells rubber ducks.

Your task is to minimize the shipping costs for your supply chain
system for a given month, and then to maximize the overall profit for
that month.

You have 3 main warehouses in Santa Fe, El Paso, and Tampa Bay. At
each warehouse, you are given a certain number of rubber ducks that
must be shipped to your stores in various cities across the US. The
number of supplies (in units of `ducks`) for each warehouse is listed
here:

Table: Supplies (in `ducks`)

| Santa Fe  | El Paso   | Tampa Bay  |
| :-------- | :-------- | :--------- |
| 700       | 200       | 200        |


You have 5 stores located across the US that will sell these ducks to
your customers. The demands at each store for the given month are as
follows (again in units of `ducks`):

Table: Demand (in `ducks`)

| Chicago   | LA   | NY   | Houston   | Atlanta   |
| :-------- | :--- | :--- | :-------- | :-------- |
| 200       | 200  | 250  | 300       | 150       |


In order to ship the rubber ducks to each of these cities, you use an
air-freight service that charges different prices between different
cities depending on how many ducks you ship. Some routes are not
available. The following grid indicates the cost per duck (in dollars)
to ship from a warehouse to a store (these routes are one-way; you
can't ship from a store back to the warehouse):

Table: Shipping costs (\$ per `duck`)

|           | Chicago | LA | NY | Houston | Atlanta |
|:----------|:--------|:---|:---|:--------|:--------|
|  Santa Fe |       6 |  3 |  - |       3 |       7 |
|   El Paso |       - |  7 |  - |       2 |       5 |
| Tampa Bay |       - |  - |  7 |       6 |       4 |

Thus e.g. it costs 6 dollars to ship a single duck from Santa Fe to
Chicago.

Now, Houston and Atlanta are hubs that -- in addition to accepting
ducks to meet their own local demand -- can also relay ducks to some
other destinations. Those routes and their associated costs are
indicated here:

Table: Relay route costs (\$ per duck)

|         | Chicago | LA | NY | Houston | Atlanta |
|:--------|:--------|:---|:---|:--------|:--------|
| Houston |       4 |  5 |  6 |       - |       2 |
| Atlanta |       4 |  - |  5 |       2 |       - |


Finally, shipping on each route is restricted to a maximum of 200
units (ducks) for the month.

The basic problem is to determine an optimum shipping plan that
minimizes the total cost of shipping while meeting all customer
demands with available supplies.  Your task will be to formulate a
linear program to solve this problem -- and some variations of this
problem --, and to enter this linear program and solve it using
``python/scipy``.

For simplicity, I'll accept answers involving partial ducks -- you
shouldn't treat this as an integer programming problem.


# Your tasks:


1. Formulate and draw a network-flow model describing this supply
   chain problem. You must explain all the constraints that you have
   included and why you have included them. You are *strongly*
   encouraged to include a node for the source of ducks (an
   ``initial`` node) and a node for the customers (a ``terminal``
   node) even though these nodes are not really involved in the
   air-freight.

2. Use your network-flow model to formulate the linear program. 

   Make sure that you include a clear description (in addition to
   code) of the objective function, the equality constraints, and the
   inequality constraints and how this data is obtained from the
   network flow.

   
   You may adapt the code given in examples in class
   (`restaurant/tablecloths` example, and `grocery store` example), or
   you may "start from scratch" and write your own code to handle this
   model.
   

3. Enter your model into ``python`` and use the ``linprog`` command
   (from ``scipy.optimize``) to find an optimal solution.  As usual, 
   you can  use ``colab`` or a ``python`` interpreter.  
   
   Be sure to include any code used in producing the specifications
   for the equality and inequality constraints. Include in your report
   the formulation of the call to ``linprog`` and the text of the
   output of that function.

4. Next, consider the following variant problems. Assume that shipping
   workers in LA are unhappy and contemplating a strike. They demand
   changes that would result in the doubling of all shipping costs to
   LA; if their demand is not met they will strike and the maximum
   number of supplies that can be shipped on *all routes to LA* is cut
   in half (i.e., from 200 to 100). Model both scenarios and see which
   one increases the cost more.

   Explain how you adapt your model to account for these scenarios.

5. Test the same scenarios contemplated in 4. on the hub city of
   Houston. Is the result more or less drastic? Which city (LA or
   Houston) would have the larger impact on costs if a work stoppage
   occurred?

6. Finally, return to the non-strike scenario, and consider the value
   of the goods being made and sold.  The following table shows the
   profit made at each city from selling 1 rubber duck. Note that in
   the warehouse cities, you are making the goods, which amounts to a
   cost rather than revenue. Now, use a related linear program to
   maximize the total profit, taking into account the shipping costs.

Table: Profit by city (in \$ per duck)

| Santa fe   | El Paso   | Tampa Bay   | Chicago   | NY   | Houston   | Atlanta   | LA   |
| :--------- | :-------- | :---------- | :-------- | :--- | :-------- | :-------- | :--- |
| -8         | -5        | -10         | 15        | 25   | 10        | 10        | 20   |

