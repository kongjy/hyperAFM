#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 12:35:55 2017

@author: Jessica
"""

import matplotlib.pyplot as plt
import numpy as np


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math


"""
-loadings happen bc theyre not real spectra
-should have positive eigenvectors and values

"""
mu = 4
mu2 = 0.5
mu3 = 0.75

variance = 2
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
B[100:140] = mlab.normpdf(x, mu, sigma).reshape(40,1)
B[305:345] =  mlab.normpdf(x3, mu3, sigma3).reshape(40,1)
B[470:510] = mlab.normpdf(x2, mu2, sigma2).reshape(40,1)
B = B.reshape(559)

C = np.zeros((559, 1))
C[158:198] = mlab.normpdf(x2, mu2, sigma2).reshape(40,1)
C[354:394] = mlab.normpdf(x, mu, sigma).reshape(40,1)
C[512:552] = mlab.normpdf(x3, mu3, sigma3).reshape(40,1)
C = C.reshape(559)

#initiate spectral and functional image
spectralmatrix = np.zeros((256, 256, 559))
functionalmatrix = np.zeros((256, 256))
Amatrix = np.zeros((256, 256))
Bmatrix = np.zeros((256, 256))
Cmatrix =np.zeros((256, 256))
xaxis = spectralmatrix.shape[0]
yaxis = spectralmatrix.shape[1]

#generate random coefficients 



#need to create matrix with a spectrum at each point. 

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
        Amatrix[x][y] = a
        Bmatrix[x][y] = b
        Cmatrix[x][y] = c

 


#need to make a matrix that is a function of the spectral matrix, which
#should be relatively easy once the spectral matrix is done. 

#run peak finding function on the spectra to identify peaks

#run Principal component analysis to find principal components 

#run Linear Regression on Principal Components 
