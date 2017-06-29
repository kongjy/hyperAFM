import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from scipy.signal import  argrelmax, detrend, sawtooth
from sklearn import cluster
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabaz_score
import matplotlib
from sklearn import decomposition

def get_hyper_peaks(hyper_image, threshold):
    """
    Given a Hyperspectral image, computes the average spectrum and finds the peaks of that spectrum.
    
    Input:
        hyper_image: An image where each pixel represents one PiFM spectrum.
        threshold: The minimum percentage to consider when finding peaks. (value 0.0 - 1.0)
    Output:
        peak_locs: the locations of the peaks in point space.
        spectrum: the computed average spectrum of the hyper image
    """
    
    im_list = []
    for i in range(hyper_image.shape[0]):
        for j in range(hyper_image.shape[1]):
            im_list.append(hyper_image[i,j,:])


    spectrum = np.column_stack(tuple(im_list)).mean(axis=-1)
    scale_threshold = threshold*spectrum.max()
    
    thresh_spec = spectrum.copy()
    thresh_spec[thresh_spec < scale_threshold] = 0


    peak_locs = argrelmax(thresh_spec, order=5)[0]
    
    return peak_locs, spectrum


def sum_around_peak(hyper_image, peak_loc, width):
    """
    """
    half_width = np.floor(width/2)
    result_array = np.zeros(hyper_image.shape[:-1])
    top = peak_loc+half_width
    bottom = peak_loc-half_width
    
    if top >= hyper_image.shape[-1]:
        top = hyper_image.shape[-1]
    if bottom < 0:
        bottom = 0
        
    indices = np.arange(bottom, top,dtype=int)
    
    for i in range(hyper_image.shape[0]):
        for j in range(hyper_image.shape[1]):
            result_array[i,j] = hyper_image[i,j,indices].sum()
            
    return result_array


def generate_features(hyper_image, peak_locs, width, filt=False):
    """
    """
    features = []
    for peak in peak_locs:
        img = sum_around_peak(hyper_image, peak, width)

        if filt == True:
            img = detrend(img, axis=1)
#            img = gaussian_filter(img, sigma=1.0)

        features.append(img.ravel())
        
    feature_array = np.column_stack(tuple(features))
    feature_array = preprocessing.scale(feature_array)
    
    return feature_array


def feature_by_pixel(hyper_image):
    x_pixels, y_pixels, spectrum_length = hyper_image.shape
    
    features = []
    for j  in range(y_pixels):
        for i in range(x_pixels):
            features.append(hyper_image[i,j,:])
    
    return np.array(features)


def kmeans_hyper(hyper_image,features, n_clusters):
    """
    """
    
    kmeans = cluster.KMeans(n_clusters=n_clusters).fit(features)
    
    label_image = kmeans.labels_.reshape(hyper_image.shape[:-1])

    kmeans_spectra = []
    for n in range(n_clusters):
        spectra = hyper_image[label_image == n]
        spectrum = spectra.mean(axis=0) 
        kmeans_spectra.append(spectrum)
        
    print calinski_harabaz_score(features, label_image.ravel())
    return label_image, kmeans_spectra


def gmm_hyper(hyper_image, features, n_clusters):
    """
    """


    gmm = GaussianMixture(n_components=n_clusters)
    gmm.fit(features)
    labels = gmm.predict(features)


    label_image = labels.reshape(hyper_image.shape[:-1])

    gmm_spectra = []
    
    for n in range(n_clusters):
        spectra = hyper_image[label_image == n]
        spectrum = spectra.mean(axis=0) 
        gmm_spectra.append(spectrum)

    print calinski_harabaz_score(features, label_image.ravel())

    return label_image, gmm_spectra


def mean_shift_hyper(hyper_image, features):
    """
    """
    bandwidth = cluster.estimate_bandwidth(features, quantile=0.2, n_samples=100)
    
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True,n_jobs=4,min_bin_freq=8)
    ms.fit(features)
    labels = ms.labels_
    label_image = labels.reshape(hyper_image.shape[:-1])
    
    n_clusters = len(np.unique(labels))
    gmm_spectra = []
    
    for n in range(n_clusters):
        spectra = hyper_image[label_image == n]
        spectrum = spectra.mean(axis=0) 
        gmm_spectra.append(spectrum)
        
    print n_clusters
    print silhouette_score(features, label_image.ravel(), sample_size=1000)
    return label_image, gmm_spectra


def report_stats(labels, channel_data):
    """
    """
    classes = np.unique(labels)
    
    results = []

    for clas in classes:
        print clas
        indices = np.where(labels == clas)

        values = channel_data[indices]
        
        results.append(values.mean())

    return results

test_mode = False
#skpm = util.load_ibw('C:\\Users\\jarrison\\OneDrive\\Documents\\hyperAFM\\Data\\SKPMcAFM_set1\\MAPIFilm12SKPM_0017.ibw')
#skpm_topo = skpm[:,:,0]


hyper_data = util.HyperImage('C:\\Users\\jarrison\\Documents\\Ion trEFM paper\\20170623 PEDOT\\EG_10mg_0017.txt')
hyper_image = hyper_data.hyper_image
wavelengths = hyper_data.wavelength_data
channel_data = hyper_data.channel_data
hyper_topo = detrend(channel_data[:,:,0],axis=1)

peaks, spectrum = get_hyper_peaks(hyper_image, 0.1)
colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'black', 'teal']

if test_mode == True:

    for width in [11,13,15]:
        for i in range(2,9):
            print str(i) + ':' + str(width)
            features = generate_features(hyper_image, peaks, width, filt=True)
            pca = decomposition.PCA(n_components=.95)
            H = pca.fit_transform(features)
            comps = pca.components_
    
            gmm, gmm_spectra = gmm_hyper(hyper_image, H, i)
            print '_'*80
else:
    
            features = generate_features(hyper_image, peaks, 13, filt=True)
            pca = decomposition.PCA(n_components=.95)
            H = pca.fit_transform(features)
            comps = pca.components_
    
            gmm, gmm_spectra = gmm_hyper(hyper_image, H, 4)
       
#features = feature_by_pixel(hyper_image)
#features = preprocessing.scale(features)    
#pca = decomposition.PCA(n_components=.95)
#H = pca.fit_transform(features)
#aa = pca.components_        
#print pca.explained_variance_ratio_
#print sum(pca.explained_variance_ratio_)       
#for i in aa:
#    plt.plot(i)      
#        
#gmm, gmm_spectra = gmm_hyper(hyper_image, H, 6)       
        
results = report_stats(gmm, hyper_topo)        
print results       
        
        
        
fig = plt.figure()
plt.imshow(hyper_topo, cmap='viridis')
plt.show()

fig = plt.figure()
cax = plt.imshow(gmm, cmap=matplotlib.colors.ListedColormap(colors[:4]))
#fig.colorbar(cax,ticks=np.arange(3))
plt.show()

offset = 0.0
plt.figure()

spectra = []
for j,spectrum in enumerate(gmm_spectra):
    spectrum += offset
    plt.plot(wavelengths, spectrum,color=colors[j])
    spectra.append(spectrum)
    offset += .0001
plt.show()

diff = []
difference = 0
labels = []
for i,spectrum1 in enumerate(spectra):
    for j,spectrum2 in enumerate(spectra):
        if i ==j:
            continue
        if i - j >0:
            continue
        string = str(i)+':'+str(j)
        labels.append(string)
        difference = spectrum1 - spectrum2

        diff.append(np.abs(difference))
        
offset = 0   
 
plt.figure()  
for j,spectrum in enumerate(diff):

    spectrum += offset
    plt.plot(wavelengths, spectrum, label=labels[j])
    spectra.append(spectrum)
    offset += .0001
plt.legend()
plt.show()

