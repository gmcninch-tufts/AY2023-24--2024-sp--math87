from graphviz import Digraph

## https://www.graphviz.org/
## https://graphviz.readthedocs.io/en/stable/index.html

dot = Digraph('fruit wholesaler model')

dot.attr(rankdir='TB')
dot.node('g','grower')

month_dict = {1:"aug",
              2:"sep",
              3:"oct",
              4:"nov",
              5:"dec",
              6:"jan",
              7:"feb",
              8:"mar",
              9:"apr",
              10:"may",
              11:"jun",
              12:"jul"}

months = list(month_dict.keys())
grow_months = months[:7]

def monthName(i):
    return month_dict[i]

with dot.subgraph(name='months') as c:
    c.attr(rank='LR')
    for month in months:
        c.node(monthName(month))

dot.node('d','demand')

# storage edges
for (m,n) in zip(months,months[1:]):
    dot.edge(monthName(m),monthName(n),label=f"s_{m}")

# purchase from grower
for m in grow_months:
    dot.edge('g',monthName(m),label=f"g_{m}")

# sales

for m in months:
    dot.edge(monthName(m),'d',label=f"d_{m}")
    
#dot.edge('g','aug',label='[-.8,15K,0]')
#dot.edge('g','sep',label='[-.55,∞,0]')
#dot.edge('g','oct',label='[-.55,∞,0]')
#dot.edge('g','nov',label='[-.65,∞,0]')
#dot.edge('g','feb',label='[-.95,15K,0]')


# dot.edge('aug','d',label='[0.9,10K,0]')
# dot.edge('sep','d',label='[0.65,15K,0]')
# dot.edge('oct','d',label='[0.65,15K,0]')
# dot.edge('nov','d',label='[0.85,15K,0]')
# dot.edge('feb','d',label='[1.20,10K,0]')
# dot.edge('mar','d',label='[1.20,10K,0]')

    
dot

dot.format='png'
dot.render()
