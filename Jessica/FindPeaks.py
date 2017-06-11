#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:40:43 2017

@author: Jessica
"""
import numpy as np
import peakutils

#needs to have format wavenumber | intensity 
def FindPeaks(spectrum, thres=0.01, min_dist=1):
    """This function takes a spectrum and identifies the absorption peaks.
    the peaks it identifies has intensity with the  minimum threshold 
    specified with spacing between peaks at least min_dist.
    
    PARAMETERS: 
        spectrum: list of intensities; you need to know the wavenumber
        range of the spectrum! 
        
        thres: minimum relative intensity required to be considered a peak.
        Only peaks with relative amplitude higher than threshold will 
        be counted.
        
        min_dist: minimum index spacing between two peaks. Setting this to
        1 means that the minimum distance between two peaks is the resolution
        of the IR spectrum, which is specified during the experiment. 
        
        Also see peakutils.peak.indexes at: 
        http://pythonhosted.org/PeakUtils/reference.html
    
    RETURNS:
        A dictionary with the peak positions and intensities. 
    
    """
    #use peak utils to find indices of peaks.
    peakindices = peakutils.indexes(spectrum, thres=thres,
                                    min_dist=min_dist)
    
    #create empty dictionary to store peak position and intensity
    peaksdict={}
    #loop through all indices identified by peakutils and store its position
    #and intensity
    for index in peakindices:
        #store each value as a 1-element list 
        peaksdict[index] = spectrum[index]
    return peakindices, peaksdict
