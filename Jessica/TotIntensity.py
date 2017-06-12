# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 18:22:47 2017

@author: Jessica
"""
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
                
    TO DO: values in dictionary are stored as lists, which can not be added.
    Change to allow for addition of intensities. 
    """
    peakindices, allpeaks = FindPeaks.FindPeaks(spectrum, thres, min_dist)
    
    totintensity = sum(allpeaks.values())
    return totintensity