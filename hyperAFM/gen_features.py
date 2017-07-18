import numpy as np
from scipy.signal import argrelmax, detrend
from scipy.integrate import trapz
from scipy.ndimage.filters import gaussian_filter
import peakutils


def get_hyper_peaks(hyper_image, threshold):
    """
    Given a Hyperspectral image, computes the average spectrum and finds the 
    peaks of that spectrum.
    
    Input:
        hyper_image: An image where each pixel represents one PiFM spectrum.
        threshold: The minimum percentage to consider when finding peaks. 
    Output:
        peak_locs: the locations of the peaks in point space.
        spectrum: the computed average spectrum of the hyper image
    """
    im_list = []
    for i in range(hyper_image.shape[0]):
        for j in range(hyper_image.shape[1]):
            im_list.append(hyper_image[i, j, :])

    spectrum = np.column_stack(tuple(im_list)).mean(axis=-1)
    scale_threshold = threshold*spectrum.max()

    thresh_spec = spectrum.copy()
    thresh_spec[thresh_spec < scale_threshold] = 0
    peak_locs = []

    peak_locs = argrelmax(thresh_spec, order=2)[0]
    peak_locs = peakutils.indexes(spectrum, thres=threshold)
    return peak_locs, spectrum


def sum_around_peak(hyper_image, peak_loc, width):
    """
    Given a hyper image, peak location, and a desired width this function
    computes the integral amplitude under each peak and returns an image of
    these values with the same dimensions as the hyperspectral image.

    Input:
        hyper_image: An image where each pixel represents one PiFM spectrum.
        peak_loc: An integer representing the location of a detected peak.
        width: total width to integrate around this peak.
    Output:
        result_array: an image of the integrated intensities with the same
            first two dimensions as the input hyperspectral data.
    """
    half_width = np.floor(width/2)
    result_array = np.zeros(hyper_image.shape[:-1])
    top = peak_loc+half_width
    bottom = peak_loc-half_width

    if top >= hyper_image.shape[-1]:
        top = hyper_image.shape[-1]
    if bottom < 0:
        bottom = 0

    indices = np.arange(bottom, top, dtype=int)
    for i in range(hyper_image.shape[0]):
        for j in range(hyper_image.shape[1]):
            result_array[i, j] = trapz(hyper_image[i, j, indices])

    return result_array


def generate_features(hyper_image, peak_locs, width, filt=False, sigma=1.0):
    """
    Converts a hyperspectral image into a feature array, where each feature is 
    the integrated intensity under a detected PiFM peak. Options included for 
    gaussian filtering of the features.
    
    Input:
        hyper_image: An image where each pixel represents one PiFM spectrum.
        peak_locs: An array of integers representing the locations detected peaks.
        width: total width to integrate around this peak.
    Output:
        feature_array: an n_sample by n_peaks feature array to apply machine 
            learning methods on.
    """
    features = []
    imgs = []
    for peak in peak_locs:
        img = sum_around_peak(hyper_image, peak, width)
        img = detrend(img, type='constant')
        if filt:
            img = gaussian_filter(img, sigma=sigma)

        features.append(img.ravel())
        imgs.append(img)
    feature_array = np.column_stack(tuple(features))

    return feature_array, imgs


def feature_by_pixel(hyper_image):
    """
    Converts a hyper image to a feature array where each sample is a PiFM 
    spectrum in its entirety.
    
    Input:
        hyper_image: An image where each pixel represents one PiFM spectrum.

    Output:
        feature_array: an n_sample by n_wavenumbers feature array.
    """
    x_pixels, y_pixels, spectrum_length = hyper_image.shape

    features = []
    for j in range(x_pixels):
        for i in range(y_pixels):
            features.append(hyper_image[j, i, :])

    return np.array(features)
