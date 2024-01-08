import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
# https://matplotlib.org/3.3.1/gallery/mplot3d/surface3d.html

def draw_graph(f,x,y,x0,y0,elev_azim=[]):
    X,Y = np.meshgrid(x,y)

    fig = plt.figure(figsize=(len(elev_azim)*10,10))
    for idx,(e,a) in enumerate(elev_azim,start=1):
        
        ax = fig.add_subplot(1,len(elev_azim),idx,projection='3d',elev=e,azim=a)
        ax.plot_wireframe(X,Y,f(X,Y))

        ax.plot(x,y0*np.ones(y.shape), zs= f(x,y0), color="red", linewidth=3)
        ax.plot(x0*np.ones(x.shape),y, zs= f(x0,y), color="red", linewidth=3)
    
    return fig

#--------------------------------------------------------------------------------
# example in which critical point gives an extrema

def f(x,y):
    return x**2 + y**2

af=draw_graph(f,
              x=np.linspace(-1,1,25),
              y=np.linspace(-1,1,25),
              x0=0,
              y0=0,
              elev_azim=[(35,15),(35,30),(35,75)])

#--------------------------------------------------------------------------------
# saddle-point example

def g(x,y):
    return x**2 - y**2

ag=draw_graph(g,
              x=np.linspace(-1,1,25),
              y=np.linspace(-1,1,25),
              x0=0,
              y0=0,
              elev_azim=[(35,15),(35,35),(35,75)])


#--------------------------------------------------------------------------------

s = np.linspace(2000,8000,25)
t = np.linspace(2000,8000,25)


def p(s,t):
    return -400000 + 144*s + 174*t - 0.01*s**2 - 0.01*t**2 - .007*s*t

a=draw_graph(p,
             x=s,
             y=t,
             x0=4735,
             y0=7043,
             elev_azim=[(45,20),(45,55)])


#--------------------------------------------------------------------------------
# countour plot

S,T = np.meshgrid(s,t)

figc = plt.figure(figsize=(20,10))
axc = figc.add_subplot()
axc.contourf(S,T,p(S,T),levels=20
             , extend='both')
axc.scatter(4735,7043,marker="X")

# A= np.array([[.02,.007],[.007,.02]])
# b=np.array([144,174])
# np.linalg.solve(A,b)
