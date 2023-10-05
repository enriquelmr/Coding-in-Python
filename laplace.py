####Electromasoquismo 1###
#Luis Enrique Martinez Rojas-elbarto2996@ciencias.unam.mx#

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


dm= 1e-6

m= np.zeros([90,90],float)
ma = np.empty([90,90],float)

m[30,30:61],m[30:61,30],m[30:61,60],m[60,30:61] = 100,100,100,100
d= 2


while(dm < d):
    for i in range(90):
        for j in range(90):
            if(i == 30 and 30 <= j < 61):
                ma[i,j] = m[i,j]
            elif(30 <= i < 61 and j == 30):
                ma[i,j] = m[i,j]
            elif(30 <= i < 61 and j == 60):
                ma[i,j] = m[i,j]
            elif(i == 60 and 30 <= j < 61):
                ma[i,j] = m[i,j]
            elif(i == 1 or j==1 or i == 89 or j == 89):
                ma[i,j] = m[i,j]
            else:
                ma[i,j] = (m[i-1,j]+m[i+1,j]+m[i,j-1]+m[i,j+1])/4

    d = np.max(abs(m-ma))
    m,ma = ma,m


plt.figure(figsize=(9,9))
plt.title(u'Lineas Equipotenciales')
imagen = plt.imshow(m,cmap ='winter')
plt.colorbar(imagen,orientation = 'vertical')
#plt.show()


fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(0, 90, 1)
Y = np.arange(0, 90, 1)
X, Y = np.meshgrid(X, Y)

Z =m[X,Y]
plt.xlabel("eje x")
plt.ylabel("eje y")
plt.title(u'Potencial electrico con respecto a coordenadas x,y')
plt.colorbar(imagen,orientation = 'vertical')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='winter')

Ex=np.zeros([90,90],float)
Ey=np.zeros([90,90],float)

for i in range(2,89):
      for j in range(2,89):
             Ex[i,j]=(-1)*((m[i,j+1]-m[i,j])/1)
             Ey[i,j]=(-1)*((m[i+1,j]-m[i,j])/1)

plt.figure(figsize=(9,9))
plt.title(u'Valores de la cordenada ex de E')
image = plt.imshow(Ex,cmap ='hot')
plt.colorbar(image,orientation = 'vertical')
#plt.show()
plt.figure(figsize=(9,9))
plt.title(u'Valores de la cordenada ey de E')
imagn = plt.imshow(Ey,cmap ='hot')
plt.colorbar(imagn,orientation = 'vertical')
#plt.show()

X,Y =np.arange(2, 89, 1), np.arange(2, 89, 1)
X,Y=np.meshgrid(X,Y)
V=Ex[X,Y]
U=Ey[X,Y]
plt.figure()
Q=plt.quiver(X, Y, U, V)
plt.title(u'Campo E')

plt.show()
