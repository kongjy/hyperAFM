#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import numpy as np 
import syntheticspectra
import FindPeaks
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA as sklearnPCA

def get_hyper_peaks(hyper_image, threshold):
    """
    Given a Hyperspectral image, computes the average spectrum and finds the peaks of that spectrum.
    
    Input:
        hyper_image: An image where each pixel represents one PiFM spectrum.
        threshold: The minimum percentage to consider when finding peaks. (value 0.0 - 1.0)
    Output:
        peak_locs: the locations of the peaks in point space.
        spectrum: the computed average spectrum of the hyper image
    """
    
    im_list = []
    for i in range(hyper_image.shape[0]):
        for j in range(hyper_image.shape[1]):
            im_list.append(hyper_image[i,j,:])


    averagespectrum = np.column_stack(tuple(im_list)).mean(axis=-1)
    
    return averagespectrum 

averagespectrum = get_hyper_peaks(spectralmatrix, threshold=0.01)

def makefeaturematrix(spectralmatrix, averagespectrum):
    """
    Makes a matrix containing peak intensities at each peak for every pixel
    from spectral matrix and its average spectrum.
    
    Input: 
        spectramatrix: matrix containing spectrum at each pixel
        average spectrum: list of average intensities at each point  
    """
    #know that all spectra are a comination of the three reference peaks
    #so their indices are known. This will not be the case for the real
    #data.
    peakindices, peaksdict = FindPeaks.FindPeaks(averagespectrum, \
                                             thres = 0.01, min_dist = 1)
    #initiate sample matrix
    xaxis = spectralmatrix.shape[0]
    yaxis = spectralmatrix.shape[1]
    featurematrix = np.zeros((xaxis**2, len(peakindices)))
    counter = -1
    #loop over elements in spectralmatrix 
    for x in range(xaxis):
        for y in range(yaxis):
            counter +=1 
            for peak in range(len(peakindices)): 
                featurematrix[counter, peak] = \
                    spectralmatrix[x,y,peakindices[peak]]
                
    return featurematrix

featurematrix = makefeaturematrix(spectralmatrix, averagespectrum)

def stdfeature(featurematrix, axis):
    """ 
    Standardizes a matrix along the specified axis to zero mean and unit 
    variance .
    """
    featurematrix_std = scale(featurematrix, axis = axis)
    
    return featurematrix_std 

#standardize matrix 
featurematrix_std = stdfeature(featurematrix, axis = 0)
#tcheck that sample matrix is standardized, use
#std.sample.mean(axis=0)
#stdsample.std(axis=0)
#along axis 0  = running vertically downwards, across rows; 1 = columns

#sklearn pca
sklearn_pca = sklearnPCA(n_components=9)
principalcomponents = sklearn_pca.fit_transform(featurematrix_std)
U =  sklearn_pca.fit_transform(featurematrix_std)
cov = sklearn_pca.get_covariance()
score = sklearn_pca.score_samples(featurematrix_std)

#matrix decomposition 
mean_vec = np.mean(featurematrix_std, axis=0)
cov_mat = np.cov(featurematrix_std.T)
eig_vals, eig_vecs = np.linalg.eig(cov_mat)

#firstsampfirstcomp = np.dot(eig_vecs[:,0], featurematrix_std[0,:]-mean_vec) 
#matches with mlPCA.Y[0,:]

##matlab pca 
from matplotlib.mlab import PCA
mlPCA = PCA(featurematrix_std)
#attribute .Y is the input projected into PCA space 
mltrans = mlPCA.Y
#reshape
mltransreshape = mltrans.reshape((256,256,9))
#check that it was reshaped correctly
#mltrans[513,:] should be the same as mltransreshape[2,1,:]

