from graphviz import Digraph as GVDigraph
import numpy as np
from scipy.optimize import linprog
import math
from dataclasses import dataclass, field

#-------------------------------
## "standard basis vector"
##
def sbv(index,size):
    return np.array([1.0 if i == index else 0.0 for i in range(size)])

def from_indices(dat,length):
    ## dat is a list [(c,i).,,,] of pairs; the pair (c,i) determines
    ## the vector c*e_i where e_i is the ith standard basis vector
    ## from_indices(dat,length) function returns the sum of the vectors 
    ## specified by the list dat
    return sum([c*sbv(i,length) for (c,i) in dat],np.zeros(length))

## >>> from_indices([(2,3),(3.5,6)],7)
## array([ 0.,  0., 2., 0.,  0.,  3.5,  0.])

#-----------------------------

def flatten(ll : list[list[any]]) -> list[any]:
    return [ i for l in ll for i in l ]

@dataclass
class UpperBound:
    bound: int = math.inf

    
@dataclass
class LowerBound:
    bound: int = -math.inf

    
@dataclass
class Edge:
    vp: (str,str)
    label: str
    val: float = 0.0
    bd: UpperBound | LowerBound = field(default=UpperBound)

@dataclass
class Digraph:
    vertices: list[list[str]]
    edges: list[Edge] 
    title: str

    def drawGraph(self):
        dot = GVDigraph(self.title)
        dot.attr(rankdir='LR')

        
        for vg in self.vertices:
            with dot.subgraph() as c:
                c.attr(rank='same')
                for x in vg:
                    c.node(x)

                    
        vv = flatten(self.vertices)
                    
        for e in self.edges:
            a,b = e.vp
            if (a in vv) and (b in vv):
                dot.edge(a,b,label=format(e.label))

        return dot
        
    
    def drawSubgraph(self,vertices:list[str] = None):
        dot = GVDigraph(self.title)
        dot.attr(rankdir='LR')

        vs = vertices if vertices else flatten(self.vertices)
        
        for x in vs:
            dot.node(x)

        for e in self.edges:
            a,b = e.vp
            if (a in vs) and (b in vs):
                dot.edge(a,b,label=format(e.label))

        return dot

    def getIncoming(self,vertex: str):
        return filter(lambda e: e.vp[1] == vertex, self.edges)
  
    def getOutgoing(self,vertex: str):
        return filter(lambda e: e.vp[0] == vertex, self.edges)

    def edgeVector(self,edge: Edge):
        i = self.edges.index(edge)
        N = len(self.edges)
        return sbv(i,N)
    
    def conservationVector(self,vertex: str):
        ivect = np.sum([self.edgeVector(e) for e in self.getIncoming(vertex)],axis=0)
        ovect = np.sum([self.edgeVector(e) for e in self.getOutgoing(vertex)],axis=0)
        return ivect - ovect

    def conservationLaw(self,vertex: str):
        ii = list(map(lambda x: x.label,self.getIncoming(vertex)))
        oo = list(map(lambda x: x.label,self.getOutgoing(vertex)))
        return "".join([ii.__repr__(),
                        " - ",
                        oo.__repr__(),
                        " = 0"])

    
    def edgeBounds(self,edge: Edge):
        match edge.bd:
            case LowerBound(bound):
                if bound > -math.inf:
                    return ((-1)*self.edgeVector(edge),(-1)*bound)
            case UpperBound(bound):
                if bound < math.inf:
                    return (self.edgeVector(edge),bound)

    def describeEdgeBound(self,edge):
        match edge.bd:
            case LowerBound(bound):
                if bound > -math.inf:
                    return edge.label + ">=" + f"{bound}"
            case UpperBound(bound):
                if bound < math.inf:
                    return edge.label + "<=" + f"{bound}"
            
                
    def allbounds(self):
        info = [self.edgeBounds(e) for e in self.edges ]
        A_ub = np.array([c[0] for c in info if c is not None])
        b_ub = np.array([c[1] for c in info if c is not None])
        return (A_ub,b_ub)

    def describeBounds(self):
        dd = map(lambda e: self.describeEdgeBound(e),self.edges)
        return [d for d in dd if not d is None]
    
    def objectiveVector(self):
        return np.sum([ e.val * self.edgeVector(e)
                        for e in self.edges if e.val is not None],
                      axis=0)

                
@dataclass(kw_only=True)
class networkFlow(Digraph):
    source: str 
    sink: str 
    

    def __post_init__(self):
        Digraph.__init__(self,vertices=self.vertices,edges=self.edges,title=self.title)

    def internalVertices(self):
        return [ v for v in flatten(self.vertices) if not v in [ self.source, self.sink]]

    def conservationMatrix(self):
        return [self.conservationVector(v) for v in self.internalVertices()]


    def conLaws(self):
        return [self.conservationLaw(v) for v in self.internalVertices()]
    
    def runLinProgr(self,maximize=False):
        A_ub,b_ub = self.allbounds()
        A_eq = self.conservationMatrix()
        if maximize:
            c = (-1)*self.objectiveVector()
        else:
            c = self.objectiveVector()
        return linprog(c,
                       A_eq=A_eq,
                       b_eq=np.zeros(len(self.internalVertices())),
                       A_ub=A_ub,
                       b_ub = b_ub)
    
vv = [ ['S'],['a','b'],['c','d'],['T']]
ee = [ Edge(('S','a'),'g1',bd=LowerBound(2),val=10),
       Edge(('S','b'),'g2',bd=LowerBound(2),val=20),
       Edge(('S','d'),'g3',bd=LowerBound(2),val=30),
       Edge(('a','c'),'g4'),
       Edge(('b','c'),'g5'),
       Edge(('c','T'),'g6',val=-10),
       Edge(('d','T'),'g7')
       ]

#nf = Digraph(vertices=vv,edges=ee)
nf = networkFlow(vertices=vv,edges=ee,title='Example',source='S',sink='T')

nf.format='png'
nf.drawGraph().render()

#nf.conservationMatrix()
#nf.allbounds()
nf.runLinProgr()
