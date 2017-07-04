from sklearn import linear_model
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import math
from math import *

mu = 0
mu2 = 0.5
mu3 = 0.75

variance = 0.5
variance2 = 1
variance3 = 1.5

sigma = math.sqrt(variance)
sigma2 = math.sqrt(variance2)
sigma3 = math.sqrt(variance3)

x = np.linspace(mu-3*variance,mu+3*variance, 40)
x2 = np.linspace(mu2-3*variance2, mu+3*variance2, 40)
x3 = np.linspace(mu2-3*variance3, mu+3*variance3, 40)

A = np.zeros((559,1))
A[20:60] = mlab.normpdf(x, mu, sigma).reshape(40,1)
A[230:270] = mlab.normpdf(x2, mu2, sigma2).reshape(40,1)
A[420:460] = mlab.normpdf(x3, mu3, sigma3).reshape(40,1)
A = A.reshape(559)

B = np.zeros((559,1))
B[23:63] = mlab.normpdf(x, mu, sigma).reshape(40,1)
B[400:440] =  mlab.normpdf(x3, mu3, sigma3).reshape(40,1)
B[470:510] = mlab.normpdf(x2, mu2, sigma2).reshape(40,1)
B = B.reshape(559)

C = np.zeros((559, 1))
C[320:360] = mlab.normpdf(x2, mu2, sigma2).reshape(40,1)
C[433:473] = mlab.normpdf(x, mu, sigma).reshape(40,1)
C[128:168] = mlab.normpdf(x3, mu3, sigma3).reshape(40,1)
C = C.reshape(559)

spectralmatrix = np.zeros((256, 256, 559))
functionalmatrix = np.zeros((256, 256))
Amatrix = np.zeros((256, 256))
Bmatrix = np.zeros((256, 256))
Cmatrix =np.zeros((256, 256))
xaxis = spectralmatrix.shape[0]
yaxis = spectralmatrix.shape[1]


#generating random coefficients
#creating a matrix with a spectrum at each point

np.random.seed(122)
a=np.random.rand(1)
b=np.random.rand(1)
c=np.random.rand(1)
spatialfrequency = (2*np.pi)/64
for x in range(xaxis):
    for y in range(yaxis):
        a = abs(np.sin(y*spatialfrequency))
        b = abs(np.sin(x*spatialfrequency) + np.sin(y*spatialfrequency))
        c = np.sin(x*spatialfrequency)**2
    #can make a, b, c as a function of x and y with some random noise
        spectralmatrix[x,y,:] = a*A + b*B + c*C
        functionalmatrix[x][y] = 2*a + b + 9*c
        Amatrix[x][y]=a
        Bmatrix[x][y]=b
        Cmatrix[x][y]=c

#creating a linear relating between the three matrices
pts=256
a=Amatrix
b=Bmatrix
c=Cmatrix
B0=0
B1=2
B2=1
B3=9
yactual=B0+B1*a+B2*b+B3*c

# reshaping and concatenating the matrices for linear regression
a=a.reshape(65536,1)
b=b.reshape(65536,1)
c=c.reshape(65536,1)
yactual=yactual.reshape(65536,1)
x1=np.concatenate((a,b), axis=1)
x=np.concatenate((x1,c), axis=1)

#performing the linear regression
regr=linear_model.LinearRegression()
s=regr.fit(x, yactual)
s.coef_[0], s.intercept_[0]
