
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

import matplotlib.cbook as cbook

from mpl_toolkits.mplot3d import Axes3D

#CALCULATING


# q = a + bi + cj + dk
class Quaternion:
  def __init__(self,a,b,c,d):
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    
  def plot(self):
    pass
    
  def print(self):
    print (self.a,self.b,self.c,self.d)
   
  def multiply(self,q):
    newA = self.a* q.a - self.b* q.b - self.c* q.c - self.d* q.d 
    newB = self.a* q.b + self.b* q.a + self.c* q.d - self.d* q.c 
    newC = self.a* q.c + self.c* q.a + self.d* q.b - self.b* q.d 
    newD = self.a* q.d + self.d* q.a + self.b* q.c - self.c* q.b
    
    return Quaternion(newA,newB,newC,newD)
    
  def square(self):
    return self.multiply(self)
  
  def add(self,q):
    return Quaternion(self.a+q.a , self.b+q.b , self.c+q.c , self.d+q.d)
  
  def modulus(self):
    return np.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

  
  def mandelbrot(self):
    new=Quaternion(0,0,0,0)
    answer=False
    bound=4 #modulus greater than this is guaranteed to explode
    i=0
    while i<50 and new.modulus() < bound:
        new = new.square().add(self)
        i+=1
        
    if new.modulus() < bound:
        answer = True
    
    return answer
    
  def julia(self,juliaConst):
    new=Quaternion(self.a,self.b,self.c,self.d)
    answer=False
    bound=4 #modulus greater than this is guaranteed to explode
    i=0
    while i<50 and new.modulus() < bound:
        new = new.square().add(juliaConst)
        i+=1
        
    if new.modulus() < bound:
        answer = True
    
    return answer


def findJulia(start,pixels,juliaConst):#returns a list of points in the julia set, considering the parameters

    size = abs( start.a *2 )#size of the volume we are looking at (length of the side of the cube)
    interval = size/pixels #1D distance between pixels

    x=start.a
    y=start.b
    z=start.c
    slice=start.d

    xEnd= x+size
    yEnd= y+size
    zEnd= z+size

    xPlot=[]
    yPlot=[]
    zPlot=[]


    while x <= xEnd:
        while y <= yEnd:
            while z <= zEnd:
                q = Quaternion(x,y,z,slice)
                if q.julia(juliaConst):
                    xPlot.append(x)
                    yPlot.append(y)
                    zPlot.append(z)
                z+=interval
            z=start.c
            y+=interval
        y=start.b
        x+=interval
        
    return [xPlot,yPlot,zPlot]



# --------------------------------------------------PARAMETERS-------------------------------------------------------------------------------------------------------------------------------------------

slice = 0 #to go from 4D to 3D we 'slice' the 4D object along a plane

juliaConstList= [Quaternion(-1,0.2,0,0),Quaternion(-0.291,-0.399,0.339,0.437),Quaternion(-0.2,0.6,0.2,0.2),Quaternion(-0.2,0.8,0,0)]
juliaConst=juliaConstList[3] #which Julia set are we looking at:   Z(n+1) = Z(n)**2 + juliaConst

start = Quaternion(-2.5,-2.5,-2.5,slice) #upper left corner of the volume we are looking at
pixels = 40 #amount of points that are checked per axis; recommended = 40 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



# --------------------------------------------------PLOTTING-------------------------------------------------------------------------------------------------------------------------------------------

result = findJulia(start,pixels,juliaConst)


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

scat = ax.scatter(result[0], result[1], result[2], c=result[1], marker='.')


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Julia set C= ('  +str(juliaConst.a) + ','+str(juliaConst.b) + ','+str(juliaConst.c) + ')')

plt.show()










#sources: http://paulbourke.net/fractals/quatjulia/
#sources: https://en.wikibooks.org/wiki/Pictures_of_Julia_and_Mandelbrot_Sets/Quaternions