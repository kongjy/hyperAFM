# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 18:20:08 2017

@author: Jessica
"""

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
