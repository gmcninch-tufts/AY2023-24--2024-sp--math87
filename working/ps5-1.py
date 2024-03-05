

from graphviz import Graph

def nodes(l):
    return [ f"{l}{n}" for n in range(4) ]

g = Graph()
g.attr(rankdir='LR')
g.filename='ps5-1a'
g.format='png'

with g.subgraph(name='U') as c:
    c.attr(rank='same')
    for n in nodes('U'):
        c.node(n)
with g.subgraph(name='V') as c:
    c.attr(rank='same')    
    for n in nodes('V'):
        c.node(n)

        
edges =  [ (0,0),
           (1,0),
           *[ (2,m) for m in range(3)],
           *[ (3,3-m) for m in range(2)]
          ]

for (n,m) in edges:
    g.edge(f"U{n}",f"V{m}")
g.render()



A = 
