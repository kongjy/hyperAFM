# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 17:02:23 2017

@author: Jessica
"""

def findshift(img, offimg):
    """
    Given two images, this function will use SciKit Image's 2D 
    Cross-Correlation to find the offset and shift the two images. 
    
    Parameters
    ----------
    
    img: ndarray
        The reference image.
    offimg: ndarray
        The offset image. 
    
    Returns
    -------
    
    shift: tuple 
            Amount (y,x) offimg is offset by. 
    error: float
            From SciKit-image: Translation invariant normalized 
            RMS error between the two images.
    diffphase: float
            From SciKit-image: Global phase difference between the 
            two images (should be zero if images are non-negative)
    """
    #find shift 
    shift, error, diffphase = register_translation(img, offimg)
    
    return shift, error, diffphase

def applyshift(offimg, shift):
    """ 
    Given a shift, this function will shift the image in
    Fourier Space. 
    
    Parameters
    ----------
    
    Returns
    -------
    
    offimg_shift: The offset image shifted in x, y space to match that 
    of the reference image.
    """ 

    offimg_shift = fourier_shift(np.fft.fftn(offimg), shift)
    offimg_shift = np.fft.ifftn(offimg_shift).real
    
    return offimg_shift 

def rot(img, deg, axes=(1,0), reshape=False, prefilter=False, output=np.float64): 
    """
    This function will rotate an image a given number of degrees
    
    Parameters
    ----------
    
    img: ndarray
        The reference image.
    deg: float
        Rotation angle in degrees. 
    prefilter:
        
    Returns
    -------
    img_rot: ndarray
        Rotated image of the same dtype and shape as the original image. 
        
    """
    img_rot = rotate(img, angle=deg, axes=axes, reshape=reshape, \
                     prefilter=prefilter, output=output)
    
    return img_rot

def optang(img, offimg, guessang, tol=1e-9):
    """
    This function maximizes the Structure Similarity Index (SSI)
    by using Scipy's Nelder-Mead Simplex algorithm.
    
    """
    
    def errormetric(guessang):
        """Minimizing this function gives the maximum Structural Similarity Index (SSI)
        with respect to the rotational degree of freedom between two images for a given spatial offset.
        """
        return 1-ssim(img, rot(offimg, deg=guessang))
    
    deg_opt = minimize(errormetric, x0=guessang, \
                       method='Nelder-Mead', tol=tol).x
    
    return deg_opt, errormetric(deg_opt)

def shiftandrotate(img, offimg, tol=1e-12, guessoff=(0,0), guessang=-2, iter=10):
    """
    Given two images, this function will shift and rotate the offset_image 
    until the  Structure Similarity Index (SSI) is maximized sufficiently. 
    SciKit Image's 2D Cross-Correlation is used to find the offset. The SSI
    is minimized by using Scipy's Nelder-Mead Simplex algorithm. 
    
    PARAMETERS:
        img: image to be used as reference
        offimg: image to be aligned with reference
        guessoff: guess pixel offset in format (y, x). 
                Can be helpful if images are severly misaligned
        guessang: guess angle offset, in degrees. 
                Negate to rotate counter clockwise. 
    """

    #apply guess shift
    offimg_shift = applyshift(offimg, guessoff)
    
    #find shift after guessshift is applied 
    offimg_shift = shift(img, offimg)
    
    #apply guess rotation
    offimg_rot = rot(offimg_shift, deg=guessang)
    
    #find rotation by maximizing SSI 
    deg_opt, errormetric = optang(img=img, offimg=offimg, guessang=guessang, tol=tol)

    #apply optimized rotation
    offimg_rot = rot(offimg_rot, deg=deg_opt)
    
    while (1-errormetric)<tol: 
        if guessang < 0: 
            offimg_shift, offimg_rot, deg_opt = shiftandrotate(img, offimg_rot, tol=tol, guessang=guessang-2)
        else: 
            offimg_shift, offimg_rot, deg_opt = shiftandrotate(img, offimg_rot, tol=tol, guessang=guessang+2)
        
    return offimg_shift, offimg_rot, deg_opt