#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:00:31 2017

@author: Jessica
"""

import numpy as np
import FindPeaks

def AllRelativeIntensities(spectrum, thres, min_dist):
    """Finds the relative intensities of every peak in the spectrum. 
    
    INPUT: spectrum: with format wavenumber|intensity, tab delimited.
        
        thres: minimum relative intensity required to be considered a peak.
        Only peaks with relative amplitude higher than threshold will 
        be counted.
        
        min_dist: minimum index spacing between two peaks. Setting this to
        1 means that the minimum distance between two peaks is the resolution
        of the IR spectrum, which is specified during the experiment. 
        
    RETURNS: Upper triangular matrix with relative peak intensities & peak
    positions. Indices correspond to the index of the peak in the spectrum. 
            
    """
    #store indices of peaks; store peak position and intensities
    peakindices, allpeaks = FindPeaks.FindPeaks(spectrum, thres, min_dist)
    
    #number of peaks
    peaks = len(allpeaks)
    
    #make empty matrix to store relative peak intensities
    relInt = np.empty((peaks,peaks))
    relPeak = np.empty((peaks,peaks))
    #initiate peak counter
    peakcounter = 0
    peakcounter2 = 0
    for peak in allpeaks:
        peakcounter += 1
        for peak2 in allpeaks:
            peakcounter2 += 1
            if peakcounter2 >= peakcounter:
                relInt[peakcounter-1][peakcounter2-1] = \
                      allpeaks[peak]/allpeaks[peak2]
                relPeak[peakcounter-1][peakcounter2-1] = \
                       peak/peak2
        peakcounter2 = 0
    return relInt, relPeak


