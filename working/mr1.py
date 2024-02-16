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

edges_source = [ { 'from': 'Source',
                   'to': c,
                   'equal': supplies[c],
                   'ship_costs': 0
                   }
                for c in warehouse_cities ]


edges_demand = [ { 'from': c,
                   'to': 'Demand',
                   'equal': demand[c],
                   'ship_costs': 0
                   }
                 for c in store_cities
                ]


ship_costs = [ [ 6   , 3   , inf , 3 , 7],
               [ inf , 7   , inf , 2 , 5],
               [ inf , inf , 7   , 6 , 4]
              ]
          
def get_costs(fr,to):
    i = warehouse_cities.index(fr)
    j = store_cities.index(to)
    return ship_costs[i][j]

edges_ship = [ { 'from': source,
                 'to': dest,
                 'ship_costs': get_costs(source,dest)
                }
              for source,dest in product(warehouse_cities,store_cities)
               if get_costs(source,dest) != inf
              ]

hubs = [ 'Houston', 'Atlanta' ]

relay_costs = [ [ 4, 5, 6, inf, 2],
                [ 4, inf, 5, 2, inf ]
                ]

def get_relay_costs(fr,to):
    i = hubs.index(fr)
    j = store_cities.index(to)
    return relay_costs[i][j]

edges_relay = [ { 'from': source,
                  'to': dest,
                  'ship_costs': get_relay_costs(source,dest)
                  }
                for source,dest in product(hubs,store_cities)
                if get_relay_costs(source,dest) != inf
               ]


edges =  edges_source + edges_demand + edges_ship + edges_relay

#--------------------------------------------------------------------------------
from graphviz import Digraph as GVDigraph

dot = GVDigraph("example")
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
  
dot.render('graph.png')
#--------------------------------------------------------------------------------

# return a standard basis vector
# these are "0-indexed" e.g. sbv(0,3) == [1,0,0]
def sbv(index,size):
    return np.array([1.0 if i == index else 0.0 for i in range(size)])


# return the objective vector for the "costs" linear program
def ship_costs_obj(edges):
    return sum([ e['ship_costs']*sbv(edges.index(e),len(edges))
                 for e in edges
                 if e['ship_costs'] != inf
                ])


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

def conservationMatrix(vertices,edges):
    return np.array([conservationLaw(v,edges) for v in interiorVertices(vertices,edges) ])


# return the edge with 'from': f and 'to': t
#
def lookupEdge(f,t,edges):
    r = list(filter(lambda x: x['from'] == f and x['to'] == t, edges))
    if r != []:
        return r[0]
    else:
        return "error"


def lookupEdgeIndex(f,t,edges):
    r = lookupEdge(f,t,edges)
    return edges.index(r)
    
def equalityConstraint(vertices,edges):
    cl = [conservationLaw(v,edges) for v in interiorVertices(vertices,edges) ]
    supply = [ supplies[w]*sbv(lookupEdgeIndex('Source',w,edges),len(edges))
               for w in warehouse_cities ]
    demand = [ demand[s]*sbv(lookupEdgeIndex(s,'Demand',edges),len(edges))
               for s in store_cities ]

    np.array(cl + supply + demand)
    
def ineqConstraints(edges):
    m = np.array([*[ sbv(edges.index(e),len(edges)) 
                     for e in edges 
                     if not upperBound(e) == math.inf ],
                  *[ -sbv(edges.index(e),len(edges))
                     for e in edges
                     if not lowerBound(e) == -math.inf ]
                 ])
    
    b = np.array([ *[ upperBound(e) 
                      for e in edges 
                      if not upperBound(e) == math.inf],
                   *[ -lowerBound(e) 
                      for e in edges 
                      if not lowerBound(e) == -math.inf]
                 ])

    return m,b

