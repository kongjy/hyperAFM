#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:00:31 2017

@author: Jessica
"""

import numpy as np
import FindPeaks


def TotIntensity(spectrum, thres, min_dist):
    """Takes a spectrum and returns summed intensity at each data point.
    
    INPUT: spectrum: list of intensities
       
        thres: minimum relative intensity required to be considered a peak.
        Only peaks with relative amplitude higher than threshold will 
        be counted.
        
        min_dist: minimum index spacing between two peaks. Setting this to
        1 means that the minimum distance between two peaks is the resolution
        of the IR spectrum, which is specified during the experiment. 
    
    RETURNS: number, reflecting sum of intensities at each wavenumber 
                in spectrum.
    """
    peakindices, allpeaks = FindPeaks.FindPeaks(spectrum, thres, min_dist)
    
    totintensity = sum(allpeaks.values())
    return totintensity


def RelIntensities(spectrum, peak1, peak2): 
    """Calculates the relative peak intensities of two peaks in a spectrum.
    
    INPUTS: spectrum: list of intensities
            peak1: index of peak 1
            peak2: index of peak 2
    RETURNS: relative intensity of peak1/peak2
    
    Takes a spectrum and the position of two peaks
    """
    #consider: peak indices or peak positions? 
    #calc relative peak intensities
    peak12 = spectrum[peak1]/spectrum[peak2]
    return peak12


def FindSamePeaks(indices, peaksdict, otherspectrum):
    """This function takes the indices of peak positions and finds the 
    intensity of those same peaks in a different spectrum. 
    
    INPUTS: indices: list of indices from FindPeaks
            peaksdict: dictionary of peak positions and intensities from 
                        FindPeaks
            otherspectrum: function will look in this spectrum for the same
                        peaks 

    RETURNS: peaksdict with the intensity of the peak in other 
             spectrum appended. 
    """
 
    for index in indices:
        key=index
        otherpeakintensity=otherspectrum[index]
        peaksdict[key].append(otherpeakintensity)
        
    return peaksdict


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


