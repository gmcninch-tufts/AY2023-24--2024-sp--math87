import numpy as np
from scipy.optimize import linprog
from math import inf
from itertools import product

warehouse_cities = [ 'Santa Fe',
                     'El Paso',
                     'Tampa Bay'
                    ]

store_cities = [ 'Chicago',
                 'LA',
                 'NY',
                 'Houston',
                 'Atlanta'
                ]

hubs = [ 'Houston', 'Atlanta' ]

vertices=[ 'Source',
           *warehouse_cities,
           *store_cities,
           'Demand'
          ]

supplies = { 'Santa Fe': 700,
             'El Paso': 200,
             'Tampa Bay': 200
             }

demand = { 'Chicago': 200,
           'LA': 200,
           'NY': 250,
           'Houston': 300,
           'Atlanta': 150
          }


def ship_costs(f,t):
    match (f,t):
        case 'Source',_:             # no shipping cost for "shipments" from source to warehouse
            return 0

        case _,'Demand':             # no shipping costs for "shipments" from store to customers
            return 0
        
        
        case 'Santa Fe','Chicago':
            return 6
        case 'Santa Fe','LA':
            return 3
        case 'Santa Fe','Houston':
            return 3
        case 'Santa Fe','Atlanta':
            return 7

        case 'El Paso','LA':
            return 7
        case 'El Paso','Houston':
            return 2
        case 'El Paso','Atlanta':
            return 5

        case 'Tampa Bay','NY':
            return 7
        case 'Tampa Bay','Houston':
            return 6
        case 'Tampa Bay','Atlanta':
            return 4

        case _:
            return inf

def relay_costs(f,t):
    match (f,t):
        case 'Houston','Chicago':
            return 4
        case 'Houston','LA':
            return 5
        case 'Houston','NY':
            return 6
        case 'Houston','Atlanta':
            return 2

        case 'Atlanta','Chicago':
            return 4
        case 'Atlanta','NY':
            return 5
        case 'Atlanta','Houston':
            return 2

        case _:
            return inf
        

edges_source = [ { 'from': 'Source',
                   'to': c,
                   }
                for c in warehouse_cities ]


edges_demand = [ { 'from': c,
                   'to': 'Demand',
                   }
                 for c in store_cities
                ]


edges_ship = [ { 'from': source,
                 'to': dest,
                }
               for source,dest in product(warehouse_cities,store_cities)
               if ship_costs(source,dest) != inf
              ]


edges_relay = [ { 'from': source,
                  'to': dest,
                 }
                for source,dest in product(store_cities,store_cities)
                if relay_costs(source,dest) != inf
               ]



edges =  edges_source + edges_ship + edges_relay + edges_demand 

#--------------------------------------------------------------------------------
from graphviz import Digraph as GVDigraph

dot = GVDigraph("example",format='png')
dot.attr(rankdir='LR')

dot.node('Source')

with dot.subgraph(name='warehouse') as c:
    c.attr(rank='same')
    for vertex in warehouse_cities:
        c.node(vertex)

with dot.subgraph(name='hubs') as c:
    c.attr(rank='same')
    for vertex in hubs:
        c.node(vertex)            
        
with dot.subgraph(name='stores') as c:
    c.attr(rank='same')
    for vertex in store_cities:
        if not (vertex in hubs):
            c.node(vertex)
            

c.node('Demand')
  
for e in edges:
#  dot.edge(e["from"],e["to"],label=f"costs {e['ship_costs']}")
  dot.edge(e["from"],e["to"])    
  
dot.render('graph')
#--------------------------------------------------------------------------------

# return a standard basis vector
# these are "0-indexed" e.g. sbv(0,3) == [1,0,0]
def sbv(index,size):
    return np.array([1.0 if i == index else 0.0 for i in range(size)])


# create the objective vector for the "costs" linear program
ship_costs_obj = sum([ ship_costs(e['from'],e['to'])*sbv(edges.index(e),len(edges))
                       for e in edges_ship])

relay_costs_obj = sum([ relay_costs(e['from'],e['to'])*sbv(edges.index(e),len(edges))
                        for e in edges_relay])

costs_obj = ship_costs_obj + relay_costs_obj

#--------------------------------------------------------------------------------
def getIncoming(vertex,edges):
    return [ e for e in edges if e["to"] == vertex ]
    
def getOutgoing(vertex,edges):
    return [ e for e in edges if e["from"] == vertex ] 

def isSource(vertex,edges):
    return getIncoming(vertex,edges) == []

def isSink(vertex,edges):
    return getOutgoing(vertex,edges) == []

def interiorVertices(vertices,edges):
    return [ v for v in vertices if not( isSource(v,edges) or isSink(v,edges) ) ]

#--------------------------------------------------------------------------------

def conservationLaw(vertex,edges):
    ii = sum([ sbv(edges.index(e),len(edges)) for e in getIncoming(vertex,edges) ])
    oo = sum([ sbv(edges.index(e),len(edges)) for e in getOutgoing(vertex,edges) ])
    return ii - oo

conservationMatrix =np.array([conservationLaw(v,edges) for v in interiorVertices(vertices,edges) ])


# return the edge from the list `edges` with 'from': f and 'to': t
#
def lookupEdge(f,t):
    r = list(filter(lambda x: x['from'] == f and x['to'] == t, edges))
    if r != []:
        return r[0]
    else:
        return "error"


def lookupEdgeIndex(f,t):
    r = lookupEdge(f,t)
    return edges.index(r)


# create equality constraint matrix for the supply (at warehouses) and demand (at stores)

Aeq_costs = np.concatenate([ conservationMatrix,
                             [ sbv(lookupEdgeIndex('Source',w),len(edges))
                               for w in warehouse_cities ],
                             [ sbv(lookupEdgeIndex(s,'Demand'),len(edges))
                               for s in store_cities ]
                            ],axis=0)
beq_costs = np.concatenate([ np.zeros(len(conservationMatrix)),
                             [ supplies[w] for w in warehouse_cities ],
                             [ demand[s] for s in store_cities ]
                            ])


# create inequality constraint matrix
# initially the only thing to account for is "can't ship more than 200 ducks"

Aub_costs = np.array([ sbv(edges.index(e),len(edges)) for e in edges_ship ]
                     + [ sbv(edges.index(e),len(edges)) for e in edges_relay ])

bub_costs = np.array([ 200 for e in edges_ship]
                     + [ 200 for e in edges_relay ] )



## run the "costs" linear program

costs_result = linprog(costs_obj,
                       A_eq = Aeq_costs,
                       b_eq = beq_costs,
                       A_ub = Aub_costs,
                       b_ub = bub_costs
                       )


def display_result(res):
    print(f"Objective value: {abs(res.fun)}")
    print("============================")
    for e in edges:
        i = edges.index(e)
        print(f"{e['from']} -> {e['to']}: {res.x[i]}")

## LA situation

## demand scenario

def LA_demand_ship_costs(f,t):
    match (f,t):
        case (_,'LA'):
            return 2*ship_costs(f,t)      ## double shipping costs to LA
        case _:
            return ship_costs(f,t)


def LA_demand_relay_costs(f,t):
    match (f,t):
        case (_,'LA'):
            return 2*relay_costs(f,t)      ## double shipping costs to LA
        case _:
            return relay_costs(f,t)

        
        
# this results in a new objective function

LA_demand_ship_costs_obj = sum([ LA_demand_ship_costs(e['from'],e['to'])*sbv(edges.index(e),len(edges))
                       for e in edges_ship])

LA_demand_relay_costs_obj = sum([ relay_costs(e['from'],e['to'])*sbv(edges.index(e),len(edges))
                        for e in edges_relay])

LA_demand_costs_obj = LA_demand_ship_costs_obj + LA_demand_relay_costs_obj

# results


LA_demand_costs_result = linprog(LA_demand_costs_obj,
                                 A_eq = Aeq_costs,
                                 b_eq = beq_costs,
                                 A_ub = Aub_costs,
                                 b_ub = bub_costs
                                 )

## strike scenario



LA_strike_Aub_costs = np.array([ sbv(edges.index(e),len(edges)) for e in edges_ship ]
                               + [ sbv(edges.index(e),len(edges)) for e in edges_relay ])

def LA_strike_capacity(e):
    match e['to']:
        case 'LA':
            return 100
        case _:
            return 200

LA_strike_bub_costs = np.array([ LA_strike_capacity(e) for e in edges_ship]
                               + [ LA_strike_capacity(e) for e in edges_relay ] )


LA_strike_costs_result = linprog(costs_obj,
                                 A_eq = Aeq_costs,
                                 b_eq = beq_costs,
                                 A_ub = LA_strike_Aub_costs,
                                 b_ub = LA_strike_bub_costs
                                 )



## Houston situation

## demand scenario

def Houston_demand_ship_costs(f,t):
    match (f,t):
        case (_,'Houston'):
            return 2*ship_costs(f,t)      ## double shipping costs to Houston
        case _:
            return ship_costs(f,t)


def Houston_demand_relay_costs(f,t):
    match (f,t):
        case (_,'Houston'):
            return 2*relay_costs(f,t)      ## double shipping costs to Houston
        case _:
            return relay_costs(f,t)

        
        
# this results in a new objective function

Houston_demand_ship_costs_obj = sum([ Houston_demand_ship_costs(e['from'],e['to'])*sbv(edges.index(e),len(edges))
                       for e in edges_ship])

Houston_demand_relay_costs_obj = sum([ relay_costs(e['from'],e['to'])*sbv(edges.index(e),len(edges))
                        for e in edges_relay])

Houston_demand_costs_obj = Houston_demand_ship_costs_obj + Houston_demand_relay_costs_obj

# results


Houston_demand_costs_result = linprog(Houston_demand_costs_obj,
                                      A_eq = Aeq_costs,
                                      b_eq = beq_costs,
                                      A_ub = Aub_costs,
                                      b_ub = bub_costs
                                      )

## strike scenario



strike_Aub_costs = np.array([ sbv(edges.index(e),len(edges)) for e in edges_ship ]
                            + [ sbv(edges.index(e),len(edges)) for e in edges_relay ])

def strike_capacity(e):
    match e['to']:
        case 'Houston':
            return 100
        case _:
            return 200

strike_bub_costs = np.array([ strike_capacity(e) for e in edges_ship]
                            + [ strike_capacity(e) for e in edges_relay ] )


Houston_strike_costs_result = linprog(costs_obj,
                                 A_eq = Aeq_costs,
                                 b_eq = beq_costs,
                                 A_ub = strike_Aub_costs,
                                 b_ub = strike_bub_costs
                                 )
### profit


def profit(e):
    match e['from'],e['to']:
        case 'Source','Santa Fe':
            return -8
        case 'Source','El Paso':
            return -5
        case 'Source','Tampa Bay':
            return -10
        case 'Chicago','Demand':
            return 15
        case 'NY','Demand':
            return 25
        case 'Houston','Demand':
            return 10
        case 'Atlanta','Demand':
            return 10
        case 'LA','Demand':
            return 20
        case _:
            return 0

sales = np.array([ profit(e) for e in edges])

profit_obj = sales - ship_costs_obj


Aeq_profit = conservationMatrix
beq_profit = np.zeros(len(conservationMatrix))


Aub_profit = np.concatenate([ [ sbv(edges.index(e),len(edges)) for e in edges_ship ],
                              [ sbv(edges.index(e),len(edges)) for e in edges_relay ],
                              [ sbv(lookupEdgeIndex('Source',w),len(edges))
                                for w in warehouse_cities ],                              
                              [ sbv(lookupEdgeIndex(s,'Demand'),len(edges))
                                for s in store_cities]
                              ]
                            , axis=0)

bub_profit = np.concatenate([ [ 200 for e in edges_ship],
                              [ 200 for e in edges_relay ],
                              [ supplies[w] for w in warehouse_cities ],
                              [ demand[s] for s in store_cities ]
                             ])



# create inequality constraint matrix
# initially the only thing to account for is "can't ship more than 200 ducks"


profit_result = linprog((-1)*profit_obj,
                        A_eq = Aeq_profit,
                        b_eq = beq_profit,
                        A_ub = Aub_profit,
                        b_ub = bub_profit)


def report(x):
    for (val,e) in zip(x,edges):
        print(f"{e['from']:10} -> {e['to']:10}:  {val: 7.2f}")
