from graphviz import Digraph
import numpy as np


class digraph:

    def __init__(self,vertices,edges,title='example'):
        self.vertices=vertices
        self.edges=edges
        self.title=title

    def drawSubgraph(self,vertices=None,labels=None):
        dot = Digraph(dg.title)
        dot.attr(rankdir='LR')

        vv = vertices if vertices else dg.vertices

        for x in vv:
            dot.node(x)

        for (a,b) in dg.edges:
            if (a in vv) and (b in vv):
                if not labels:
                    dot.edge(a,b)
                else:
                    dot.edge(a,b,label=labels((a,b))

        return dot

class digraphWithCapacity:

    def __init__(self,vertices,edges,cap,title='example'):
        self.vertices=vertices
        self.edges=edges
        self.cap=cap
        self.title=title

    def drawSubgraph(self,vertices=None):
        dot = Digraph(dg.title)
        dot.attr(rankdir='LR')

        vv = vertices if vertices else dg.vertices
        
        for x in vv:
            dot.node(x)

        for (a,b) in dg.edges:
            if (a in vv) and (b in vv):
                try: 
                    cab = self.cap[(a,b)]
                    dot.edge(a,b,label=format(cab))
                except:
                    dot.edge(a,b)

        return dot

class networkFlow(digraphWithCapacity):

    def __init__(self,vertices,edges,cap,source,sink,title='example'):
        digraphWithCapacity.__init__(self,vertices,edges,cap,title)
        self.source = source
        self.sink= sink
        self.check()

    def getIncoming(self,vertex):
        return filter(lambda v: v[1] == vertex, self.edges)
  
    def getOutgoing(self,vertex):
        return filter(lambda v: v[0] == vertex, self.edges)
  
    def getCap(self,edge):
        try:
            return self.cap[edge]
        except:
            return 0
      
    def sumCap(self,edgeList):
        return np.sum(np.array(list(map(self.getCap,edgeList))))

    def checkVertex(self,vertex):
        input = self.sumCap(self.getIncoming(vertex))
        output = self.sumCap(self.getOutgoing(vertex))
        if input != output:
            raise ValueError(f"conservation law fails for vertex {vertex}")

    def check(self):
        for v in self.vertices:
            if not v in [self.source,self.sink]:
                self.checkVertex(v)


vv = [ 'S','a','b','c','d','T']
ee = [ ('S','a'),
       ('S','b'),
       ('S','d'),
       ('a','c'),
       ('b','c'),
       ('c','T'),
       ('d','T')
      ]

cc = { ('S','a'):1,
       ('S','b'):1,
       ('S','d'):2,
       ('a','c'):1,
       ('b','c'):1,
       ('c','T'):2,
       ('d','T'):2
      }


nf = networkFlow(vv,ee,cc,source='S',sink='T')
