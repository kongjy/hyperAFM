#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import numpy as np 
import syntheticspectra
import FindPeaks
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA as sklearnPCA
from matplotlib.mlab import PCA

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



def stdfeature(featurematrix, axis):
    """ 
    Standardizes a matrix along the specified axis to zero mean and unit 
    variance .
    """
    featurematrix_std = scale(featurematrix, axis = axis)
    
    return featurematrix_std 

