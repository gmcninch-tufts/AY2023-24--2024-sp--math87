import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 19})

# plot the feasible region
d = np.linspace(0,11,500)
e = np.linspace(0,11,500)

xx,yy = np.meshgrid(d,e)

fig,ax = plt.subplots(figsize=(15,15))
ax.imshow(((yy >= 1) & (yy <= 9) & (9 <= 2*xx + yy) & (2*xx + yy <= 25) & (-1 <= 2*xx - yy) &
           (2*xx - yy <= 15)
           ).astype(int),
          extent=(xx.min(),xx.max(),yy.min(),yy.max()),
          origin="lower", 
          cmap="Reds", 
          alpha = 0.2)

# plot the lines defining the constraints

def l1(x): return 25 - 2*x

def l2(x): return 9 - 2*x

def l3(x): return 2*x + 1

def l4(x): return 2*x - 15

x = np.linspace(5.5,11,500)
ax.plot(x, l1(x) , label="2x + y = 25")

x = np.linspace(0,6.5,500)
ax.plot(x, l2(x) , label="2x + y = 9")

x = np.linspace(0,6.5,500)
ax.plot(x, l3(x), label = "2x - y = -1")

x = np.linspace(5.5,11,500)
ax.plot(x, l4(x), label = "2x - y = 15")

ax.axhline(y=1, color = "black")
ax.axhline(y=9, color = "black")

ax.legend()
ax.set_title("Feasible Region")
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")

def ann_pt(x,y):
    "annotate the point (x,y)"
    s = f"({x},{y})"
    ax.annotate(s,xy=(x,y),xytext=(5,5),textcoords='offset points')

ax.scatter(8, 9,s=100,color="blue")
ann_pt(8,9)

ax.scatter(4,9,s=100,color="blue")
ann_pt(4,9)

ax.scatter(4,1,s=100,color="blue")
ann_pt(4,1)

ax.scatter(8,1,s=100,color="blue")
ann_pt(8,1)

ax.scatter(2,5,s=100,color="blue")
ann_pt(2,5)

ax.scatter(10,5,s=100,color="blue")
ann_pt(10,5)

fig.savefig("feasible.png")
