import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter, argrelmax, detrend, find_peaks_cwt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture
import sklearn.decomposition
from sklearn.metrics import explained_variance_score
import matplotlib

def get_hyper_peaks(hypir_image, threshold):
    """
    """
    
    im_list = []
    for i in range(hypir_image.shape[0]):
        for j in range(hypir_image.shape[1]):
            im_list.append(hypir_image[i,j,:])


    spectrum = np.column_stack(tuple(im_list)).mean(axis=-1)
    scale_threshold = threshold*spectrum.max()
    
    thresh_spec = spectrum.copy()
    thresh_spec[thresh_spec < scale_threshold] = 0


    peak_locs = argrelmax(thresh_spec, order=1)[0]
    
    return peak_locs, spectrum



def sum_around_peak(hypir_image, peak_loc, width):
    """
    """
    half_width = np.floor(width/2)
    result_array = np.zeros(hypir_image.shape[:-1])
    
    indices = np.arange(peak_loc-half_width, peak_loc+half_width,dtype=int)
    
    for i in range(hypir_image.shape[0]):
        for j in range(hypir_image.shape[1]):
            result_array[i,j] = hypir_image[i,j,indices].sum()
            
    return result_array


def kmeans_hyper(hyper_image, peak_locs, n_clusters):
    """
    """
    features = []
    for peak in peak_locs:
        img = sum_around_peak(s, peak, 11)
        img = detrend(img)
        features.append(img.ravel())
        
    wah = np.column_stack(tuple(features))
    wah = preprocessing.scale(wah)
    kmeans = KMeans(n_clusters=n_clusters).fit(wah)
    
    label_image = kmeans.labels_.reshape(hyper_image.shape[:-1])

    kmeans_spectra = []
    for cluster in range(n_clusters):
        spectra = s[label_image == cluster]
        spectrum = spectra.mean(axis=0) 
        kmeans_spectra.append(spectrum)

    return label_image, kmeans_spectra


def gmm_hyper(hyper_image, peak_locs, n_clusters):
    """
    """
    features = []
    for peak in peak_locs:
        img = sum_around_peak(s, peak, 11)
        img = detrend(img)
        features.append(img.ravel())
        
    wah = np.column_stack(tuple(features))
    wah = preprocessing.scale(wah)
    
    gmm = GaussianMixture(n_components=n_clusters).fit(wah).predict(wah)

    label_image = gmm.reshape(hyper_image.shape[:-1])

    gmm_spectra = []
    
    for cluster in range(n_clusters):
        spectra = s[label_image == cluster]
        spectrum = spectra.mean(axis=0) 
        gmm_spectra.append(spectrum)

    return label_image, gmm_spectra

skpm_data = util.load_ibw('C:\\Users\\Cypher\\OneDrive\\Documents\\hyperAFM\\Data\\SKPMcAFM_set2\\MAPIFilm12SKPM_0017.ibw')


hyper_data = util.HyperImage('C:/Users/Cypher/Documents/Set 2/Film12topo_0058.txt')
channel_data = np.rot90(hyper_data.channel_data, k=-1)[:,::-1,:]
hyper_image = np.rot90(hyper_data.hyper_image, k=-1)[:,::-1,:]

#peaks, spectrum = get_hyper_peaks(s, 0.05)

new_skpm = util.align_images(hyper_image, skpm_data)

#colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'burlywood', 'chartreuse']
#
#label_image, kmeans_spectra = kmeans_hyper(s, peaks, 8)
#
#plt.figure()
#offset = 0.0
#for i,spectrum in enumerate(kmeans_spectra):
#    spectrum += offset
#    plt.plot(spectrum,color=colors[i])
#    offset += .0001
#plt.show()
#
#fig = plt.figure()
#cax = plt.imshow(label_image, cmap=matplotlib.colors.ListedColormap(colors))
#fig.colorbar(cax,ticks=np.arange(8))
#plt.show()
#
#colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
#gmm, gmm_spectra = gmm_hyper(s, peaks, 6)
#
#fig = plt.figure()
#cax = plt.imshow(gmm, cmap=matplotlib.colors.ListedColormap(colors))
#fig.colorbar(cax,ticks=np.arange(6))
#plt.show()
#
#offset = 0.0
#plt.figure()
#for i,spectrum in enumerate(gmm_spectra):
#    spectrum += offset
#    plt.plot(spectrum,color=colors[i])
#    offset += .0001
#plt.show()
