import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import  argrelmax, detrend
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth
from sklearn import preprocessing
from sklearn.mixture import BayesianGaussianMixture
from sklearn.metrics import silhouette_score
import matplotlib
from sklearn import decomposition

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


def generate_features(hyper_image, peak_locs, width):
    """
    """
    features = []
    for peak in peak_locs:
        img = sum_around_peak(hyper_image, peak, width)
        img = detrend(img)
        features.append(img.ravel())
        
    feature_array = np.column_stack(tuple(features))
    feature_array = preprocessing.scale(feature_array)
    
    return feature_array


def kmeans_hyper(features, n_clusters):
    """
    """
    
    kmeans = KMeans(n_clusters=n_clusters).fit(features)
    
    label_image = kmeans.labels_.reshape(hyper_image.shape[:-1])

    kmeans_spectra = []
    for cluster in range(n_clusters):
        spectra = hyper_image[label_image == cluster]
        spectrum = spectra.mean(axis=0) 
        kmeans_spectra.append(spectrum)
        
    
    return label_image, kmeans_spectra


def gmm_hyper(hyper_image, features, n_clusters):
    """
    """
    pca = decomposition.PCA(svd_solver='full',n_components=.95)
    features = pca.fit_transform(features)

    gmm = BayesianGaussianMixture(n_components=n_clusters).fit(features).predict(features)

    label_image = gmm.reshape(hyper_image.shape[:-1])

    gmm_spectra = []
    
    for cluster in range(n_clusters):
        spectra = hyper_image[label_image == cluster]
        spectrum = spectra.mean(axis=0) 
        gmm_spectra.append(spectrum)
        
    print silhouette_score(features, label_image.ravel(), sample_size=10000)

    return label_image, gmm_spectra


def mean_shift_hyper(hyper_image, features):
    """
    """
    bandwidth = estimate_bandwidth(features, quantile=0.2, n_samples=500)
    
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(features)
    labels = ms.labels_
    label_image = labels.reshape(hyper_image.shape[:-1])
    
    n_clusters = len(np.unique(labels))
    gmm_spectra = []
    
    for cluster in range(n_clusters):
        spectra = hyper_image[label_image == cluster]
        spectrum = spectra.mean(axis=0) 
        gmm_spectra.append(spectrum)
        
    print n_clusters

    return label_image, gmm_spectra


skpm = util.load_ibw('C:\\Users\\jarrison\\OneDrive\\Documents\\hyperAFM\\Data\\SKPMcAFM_set1\\MAPIFilm12SKPM_0017.ibw')
skpm_topo = skpm[:,:,0]


hyper_data = util.HyperImage('C:\\Users\\jarrison\\Downloads\\Set 1\\Set 1\\Film5_0049.txt')
hyper_image = hyper_data.hyper_image
channel_data = hyper_data.channel_data
hyper_topo = detrend(channel_data[:,:,0])

new_skpm = util.align_images(channel_data, skpm)
new_skpm_topo = new_skpm[:,:,0]

peaks, spectrum = get_hyper_peaks(hyper_image, 0.05)

features = generate_features(hyper_image, peaks, 13)

gmm, gmm_spectra = mean_shift_hyper(hyper_image, features)

colors = ['red', 'blue', 'green', 'purple']#, 'orange', 'cyan']


fig = plt.figure()
cax = plt.imshow(gmm, cmap=matplotlib.colors.ListedColormap(colors))
fig.colorbar(cax,ticks=np.arange(4))
plt.show()

offset = 0.0
plt.figure()
for i,spectrum in enumerate(gmm_spectra):
    spectrum += offset
    plt.plot(spectrum,color=colors[i])
    offset += .0001
plt.show()
