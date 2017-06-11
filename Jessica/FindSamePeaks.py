# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 18:47:52 2017

@author: Jessica
"""

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