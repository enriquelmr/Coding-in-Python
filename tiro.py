# -*- coding: utf-8 -*-
from numpy.random import randint
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random


plt.title('Tiro al blanco')
plt.xlabel('x')
plt.ylabel('y')
x = np.arange(-10,10,0.1)
y=(3*np.sqrt(80-x*x))/4
y1=-(3*np.sqrt(80-x*x))/4
z=(3*np.sqrt(32-x*x))/4
z1=-(3*np.sqrt(32-x*x))/4
w=(3*np.sqrt(16-x*x))/4
w1=-(3*np.sqrt(16-x*x))/4
u=(3*np.sqrt(4-x*x))/4
u1=-(3*np.sqrt(4-x*x))/4
plt.plot(x,y,x,y1,x,z,x,z1,x,w,x,w1,x,u,x,u1)

num1=randint(-10,10)
num2=randint(-10,10)
num3=randint(-10,10)
num4=randint(-10,10)
num6=randint(-10,10)

numi1=randint(-7,7)
numi2=randint(-7,7)
numi3=randint(-7,7)
numi4=randint(-7,7)
numi5=randint(-7,7)

jugador1=array[num1,numi1]
print jugador1
plt.show()