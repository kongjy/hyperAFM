import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter, argrelmax, detrend
from sklearn.cluster import KMeans

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


    peak_locs = argrelmax(thresh_spec, order=3)[0]
    
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
        img = sum_around_peak(s, peak, 25)
        img = detrend(img)
        features.append(img.ravel())
        
    wah = np.column_stack(tuple(features))
    
    kmeans = KMeans(n_clusters=n_clusters).fit(wah)
    
    label_image = kmeans.labels_.reshape((256,256))

    kmeans_spectra = []
    for cluster in range(n_clusters):
        spectra = s[label_image == cluster]
        spectrum = spectra.mean(axis=0)
        kmeans_spectra.append(spectrum)

    return label_image, kmeans_spectra

s = util.load_hyper_numpy('C:\\Users\\jarrison\\OneDrive\\Documents\\hyperAFM\\Data\\Film12topo_0058_numpy\\')
s = np.rot90(s,k=-1)
peaks, spectrum = get_hyper_peaks(s, .1)

label_image, kmeans_spectra = kmeans_hyper(s, peaks, 6)

plt.figure()
for spectrum in kmeans_spectra:
    plt.plot(spectrum)
plt.show()

plt.figure()
plt.imshow(label_image)
plt.show()


