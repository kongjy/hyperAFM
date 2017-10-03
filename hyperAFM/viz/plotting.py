# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 10:52:29 2017

@author: Jessica
"""

import matplotlib.pyplot as plt

def showsave(img, filename, cmap = 'viridis', colorbar = True):
    fig = plt.imshow(img, cmap = cmap)
    imgstd = img.std()
    imgmean = img.mean()
    ll = imgmean - (2*imgstd)
    ul = imgmean + (2*imgstd)
    plt.clim(ll,ul)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    if colorbar == True:
        plt.colorbar()
    plt.savefig(filename + '.png')
    return 