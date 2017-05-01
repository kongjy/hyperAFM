#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:00:31 2017

@author: Jessica
"""

import numpy as np
import FindPeak

spectrum=np.genfromtxt('../Data/PointSpectra/Spectrum1.txt', delimiter='',
                     skip_header=1)
allthepeaks=FindPeak.FindPeaks(spectrum, thres=0.0007, min_dist=1)


def TotIntensity(spectrum, thres, min_dist):
    """Takes a spectrum and returns summed intensity at each data point.
        INPUT: spectrum with format wavenumber|intensity, tab delimited.
        RETURNS: number, reflecting sum of intensities at each wavenumber 
                in spectrum.
    """
    peakindices, allpeaks = FindPeak.FindPeaks(spectrum, thres, min_dist)
    
    totintensity = sum(allpeaks.values())
    return totintensity

def RelativeIntensities(spectrum, thres, min_dist):
    """Finds the relative intensities of every peak in the spectrum. 
    
    INPUT:
    RETURNS: Upper triangular matrix with relative peak intensities & peak
    positions. Indices correspond to the index of the peak in the spectrum. 
            
    """
    #store indices of peaks; store peak position and intensities
    peakindices, allpeaks = FindPeak.FindPeaks(spectrum, thres, min_dist)
    
    #number of peaks
    peaks = len(allpeaks)
    
    #make empty matrix to store relative peak intensities
    relInt = np.empty((peaks,peaks))
    relPeak = np.empty((peaks,peaks))
    #initiate peak counter
    peakcounter = 0
    peakcounter2 = 0
    for peak in allpeaks:
        peakcounter +=1
        for peak2 in allpeaks:
            peakcounter2 += 1
            if peakcounter2 >= peakcounter:
                relInt[peakcounter-1][peakcounter2-1]=allpeaks[peak]/allpeaks[peak2]
                relPeak[peakcounter-1][peakcounter2-1]=peak/peak2
            #print(peakcounter, peakcounter2)
        peakcounter2 = 0
    return relInt, relPeak
