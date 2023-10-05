from matplotlib.patches import Ellipse
from matplotlib.patches import Polygon
import matplotlib as mpl
from pylab import *
from matplotlib import pyplot as plt
mean = [ 5, 5 ]
width = 10
height = 10
angle = 45
ell = mpl.patches.Rectangle(xy=mean, width=width, height=height, angle = 0+angle)
fig, ax = plt.subplots()
plt.title('Metrica d_{infinity}')
ax.add_patch(ell)
ax.set_aspect('equal')


ax.autoscale()
plt.show()
