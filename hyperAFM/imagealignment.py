# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 17:02:23 2017

@author: Jessica
"""
import numpy as np
from scipy import signal, optimize
from scipy.ndimage import rotate
from skimage.measure import compare_ssim as ssim
from skimage.feature import register_translation
from scipy.ndimage import fourier_shift
from scipy.optimize import minimize
from scipy.signal import detrend
from dipy.align.imaffine import AffineMap, MutualInformationMetric, \
                                AffineRegistration
from dipy.align.transforms import AffineTransform2D, RigidTransform2D, \
                            RotationTransform2D, ScalingTransform2D, \
                            TranslationTransform2D
            

def flatten(img):
    """
    Removes average from each line along the x-axis within the image. 
    
    Parameters
    ----------
    img : ndarray
        Image to be flattened
        
    Returns
    -------
    img_flattened : ndarray
            
    """
    img_flattened = detrend(img, axis=1, type='linear')
    
    return img_flattened 

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
    
    shift : tuple 
            Amount (y,x) offimg is offset by. 
    error : float
            From SciKit-image: Translation invariant normalized 
            RMS error between the two images.
    diffphase : float
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
    
    offimg_shift : The offset image shifted in x, y space to match that 
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
    
    img : ndarray
        The reference image.
    deg : float
        Rotation angle in degrees. 
    prefilter :
        
    Returns
    -------
    img_rot : ndarray
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
        """Minimizing this function gives the maximum Structural Similarity
        Index (SSI) with respect to the rotational degree of freedom between
        two images for a given spatial offset.
        """
        return 1-ssim(img, rot(offimg, deg=guessang))
    
    deg_opt = minimize(errormetric, x0=guessang, \
                       method='Nelder-Mead', tol=tol).x
    
    return deg_opt, errormetric(deg_opt)

def shiftandrotate(img, offimg, aux, tol=1e-12, guessoff=(0,0), guessang=-2, iter=10):
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
    aux_shift = applyshift(aux, guessoff
                           )
    #find shift after guessshift is applied 
    shift = findshift(img, offimg)
    
    #apply guess rotation
    offimg_rot = rot(offimg_shift, deg=guessang)
    aux_rot = rot(aux_shift, deg=guessang)
    
    #find rotation by maximizing SSI 
    deg_opt, errormetric = optang(img=img, offimg=offimg_rot, guessang=guessang, tol=tol)

    #apply optimized rotation
    offimg_rot = rot(offimg_rot, deg=deg_opt)
    aux_rot = rot(aux, deg=deg_opt)
    
    while (1-errormetric)<tol: 
        if guessang < 0: 
            offimg_shift, offimg_rot, deg_opt, aux_rot = shiftandrotate(img, offimg_rot, tol=tol, guessang=guessang-2)
        else: 
            offimg_shift, offimg_rot, deg_opt, aux_rot = shiftandrotate(img, offimg_rot, tol=tol, guessang=guessang+2)
        
    return offimg_shift, offimg_rot, deg_opt, aux_rot


def setup_mutualinformation(nbins = 32, sampling_prop = None): 
    """
    This sets up the number of bins and the percentage of pixels
    that are used to approximate the joint and marginal probability
    distribution functions (PDFS). A typical value is 32. 
    
    For more information see:
        http://nipy.org/dipy/examples_built/affine_registration_3d.html 
    and: 
        https://link.springer.com/article/10.1023/A:1007958904918
    
    Parameters
    ----------
    nbins : int
        No. bins used to approx PDFs. Default is 32. 
    
    sampling_prop : integer in range (0,100]
        percentage of pixels to be used for calculating PDFs. 
        Default is None which is 100. 
    
    Returns
    -------
    metric : class 
       Mutual Information metric used as error metric for affine
       registration 
    """
    metric = MutualInformationMetric(nbins, sampling_prop)

    return metric

def setup_affine(metric = None, level_iters = None , sigmas = None, \
                 factors = None, method = 'L-BFGS-B'):
    """
    Sets up the Gaussian Pyramid used in multi-resolution image registration
    and initializes and instance of the AffineRegistration class in dipy.

    Parameters
    ----------    
    metric : None or object, optional 
        If none, Mutual Information Metric will be used with default settings.
        Can set up with specific nbins and sampling proportion with 
        setup_mutualinformation function.
    level_iters : sequence of integers, optional 
        number of iterations at each level of pyramid. If none, the iterations
        will be [10000, 1000, 100]. 
    sigmas : sequence of floats, optional 
        smoothing paramter for each level of pyramid. Default sequence is
        [3, 1, 0], which means the image at the coarsest (see factors) level
        is smoothed the most and the image at the finest level is not smoothed.
    factors: sequence of floats, optional 
        sub-sampling factors in Gaussian pyramid. Default is [4, 2, 1] which 
        means the image at the coarsest level is a quarter the resolution and
        the image at the finest level is the original resolution. 
    method : string, optional
        optimization method used in registration. Default is L-BFGS-B but
        any gradient-based method in dipy.core.Optimize such as CG, BFGS, 
        Newton-CG, dogleg, or trust-ncg are available. 
 
    Returns
    -------
    affreg : class 
        
    """
    affreg = AffineRegistration(metric=metric, level_iters=level_iters, \
                                sigmas=sigmas, factors=factors, \
                                method = method)
    return affreg

def find_affine(static, moving, affreg, transform, \
                params0 = None, starting_affine = None): 
    """
    Uses output from setup_affine to find the optimal affine transformation 
    that maps the static image to the moving image. 
    
    Parameters
    ----------  
    static : ndarray
        reference image
    moving : ndarray
        moving image to be registered with static image
    affreg : class 
        output from setup_affine
    transform : 
        type of transformation. Can be any of the following:
        AffineTransform2D, RigidTransform2D, RotationTransform2D,
        ScalingTransform2D, TranslationTransform2D
    params0 : ndarray, shape(n,)
        parameters used to start optimization. Default is None, which means
        the optimization will start at the identity transformation. 
    starting_affine : class
        output from find_affine using a different method. 
    
    Returns
    -------
    transformation: ndarray
    """
    if starting_affine == None:
        transformation = affreg.optimize(static, moving, transform, params0)
    else: 
        transformation =  affreg.optimize(static, moving, transform, params0,\
                                     starting_affine = starting_affine.affine)
    return transformation

def apply_affine(moving, transformation):
    """
    Applies the optimized transformation found using find_affine to 
    the moving image.
    
    Parameters
    ----------  
    moving : ndarray
        moving image to be registered with static image
    transformation : class
        output from find_affine 
    Returns
    -------
    moving_transformed : ndarray
        moving image, transformed 
    """
    moving_transformed = transformation.transform(moving)
    
    return moving_transformed 

        