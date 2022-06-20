import numpy as np
import random as rd
import math
import matplotlib.pyplot as plt
# %matplotlib inline

x=np.linspace(0.05,100,400)
num=len(x)
y1=np.zeros(num)
y2=np.zeros(num)
rd.seed(2)

# rd.seed(2) produces the same random numbers
# even in every execution.
# If using as rd.seed(), the different random numbers
# will be obtained per execution.
for i in range(0,num):
    j=x[i]
    y1[i]=math.log(j)
    noise=rd.uniform(-1,1)
    y2[i]=y1[i]+noise

plt.plot(x, y1)
plt.show( )
plt.scatter(x, y2, c='red', s=40)
plt.show( )

fitting=np.polyfit(np.log(x),y2,1)
print(fitting)

# printing result is [0.97735663 0.09426108]
# A=0.97735663, B=0.09426108

A=0.97735663
B=0.09426108
logfit=np.zeros(num)

for i in range (num):
    logfit[i]=A*math.log(x[i])+B

plt.scatter(x, y2, c='red', s=40)
plt.plot(x, logfit)
plt.show( )