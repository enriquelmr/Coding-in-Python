#!/usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib.patches import Ellipse
from matplotlib.patches import Polygon
import matplotlib as mpl
from pylab import *
from matplotlib import pyplot as plt

print("hola, que metrica quieres plotear, la d_{1}, d_{2} o la infinita!!")
print("Selecciona \n 1 \n 2 o \n3")
respuesta=int(input())
print ("Haz seleccionado",respuesta)
print("Ahora introduce el radio de la metrica ")
radio=input()
print("ahora el centro en coordenadas x,y en orden")
x=input()
y=input()
print(radio)

if respuesta >=1:
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


elif(respuesta == 2):
    mean = [x,y]
    width = radio
    height = radio
    angle = 0
    ell = mpl.patches.Ellipse(xy=mean, width=width, height=height, angle = 0+angle)
    fig, ax = plt.subplots()

    plt.title('Metrica d_{2}')
    ax.add_patch(ell)
    ax.autoscale()
elif(respuesta == 3):
    mean = [ -(x/2),  -(y/2)]
    width = x
    height = y
    angle = 45
    ell = mpl.patches.Rectangle(xy=mean, width=width, height=height, angle = 0+angle)
    fig, ax = plt.subplots()

    plt.title('Metrica d_{infinity}')
    ax.add_patch(ell)
    ax.autoscale()
else:
	print("Eso no lo puedo plotear")

   

plt.show()



        
