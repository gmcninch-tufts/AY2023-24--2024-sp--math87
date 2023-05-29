from graphviz import Digraph

dg = Digraph(engine='neato')
dg.attr(rankdir='LR')

dg.node('t')

with dg.subgraph() as c:
    c.attr(rank='same')
    for x in ['a','c']:
        c.node(x)

with dg.subgraph() as c:
    c.attr(rank='same')
    for x in ['b','d']:
        c.node(x)


dg.edge('s','a','16')
dg.edge('s','c','13')

dg.edge('c','a','4')
dg.edge('a','c','10')

dg.edge('a','b','12')
dg.edge('c','d','14')

#dg.edge('b','c','9')

dg.edge('d','b','7')
dg.edge('b','d','6')

dg.edge('b','t','20')
dg.edge('d','t','4')

dg.format='png'
dg.render()



