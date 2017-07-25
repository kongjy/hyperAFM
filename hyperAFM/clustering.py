import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend
from sklearn import cluster
from sklearn import preprocessing
from sklearn.mixture import BayesianGaussianMixture, GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabaz_score
import matplotlib
from sklearn import decomposition
from itertools import cycle
from gen_features import generate_features, get_hyper_peaks, feature_by_pixel

def average_spectra(hyper_image, labels):
    """
    Gets the average spectrum of each label.
    """
    spectra_array = []
    n_labels = len(np.unique(labels))
    label_image = labels.reshape(hyper_image.shape[:-1])

    for n in range(n_labels):
        spectra = hyper_image[label_image == n]
        spectrum = spectra.mean(axis=0) 
        spectra_array.append(spectrum)
  
    return spectra_array
        

def kmeans_hyper(hyper_image,features, n_clusters):
    """
    """
    
    spec = cluster.MiniBatchKMeans(n_clusters=n_clusters, batch_size=1000,init_size=1000,n_init=1)
    spec.fit(features)  
    labels = spec.labels_ 

    kmeans_spectra = average_spectra(hyper_image, labels)
    
    score = calinski_harabaz_score(features, labels)
    
    label_image = labels.reshape(hyper_image.shape[:-1])

    return label_image, kmeans_spectra, score


def gmm_hyper(hyper_image, features, n_clusters):
    """
    """

    gmm= BayesianGaussianMixture(n_components=n_clusters, covariance_type='spherical').fit(features)
    labels = gmm.predict(features)


    label_image = labels.reshape(hyper_image.shape[:-1])

    gmm_spectra = average_spectra(hyper_image, labels)

    score = calinski_harabaz_score(features, label_image.ravel())

    return label_image, gmm_spectra, score


def dummy_cluster(hyper_image, features, n_clusters):
    """
    """

    cls = cluster.AgglomerativeClustering(n_clusters=n_clusters)
    cls.fit(features)
    labels = cls.labels_


    label_image = labels.reshape(hyper_image.shape[:-1])

    gmm_spectra = average_spectra(hyper_image, labels)

    score = calinski_harabaz_score(features, label_image.ravel())

    return label_image, gmm_spectra, score


def best_clusters(hyper_image, features, cluster_func, max_clusters=8):
    """
    Select the best number of clusters to use based on the calinski-harabaz score.
    """
    max_score = 0
    best_nclusters = 0
    all_scores = []
    for n in range(2, max_clusters + 1):
        print n
        label_image, label_spectra, score = cluster_func(hyper_image, features, n)
        all_scores.append(score)
        if score > max_score:
                max_score = score
                best_nclusters = n
        print score
    return best_nclusters, max_score, all_scores

test_mode = True
#test_mode = False

hyper_data = util.HyperImage('C:\Users\jarrison\Documents\Ion trEFM paper\\20170710 p3ht with peo\\p3ht_25PEO_0005.txt')

hyper_image = hyper_data.hyper_image[:,:,:]
wavelengths = hyper_data.wavelength_data
channel_data = hyper_data.channel_data
hyper_topo = detrend(channel_data[:,:,0],axis=1)

peaks, spectrum = get_hyper_peaks(hyper_image, 0.1)
plt.figure()
plt.plot(wavelengths, spectrum*1e3)
plt.plot(wavelengths[peaks], spectrum[peaks]*1e3,'bo')
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('PiFM Signal (mV)')
plt.show()
colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'black', 'teal']

max_score = 0
string_loc = ''

if test_mode == True:
    features, imgs =  generate_features(hyper_image, peaks, 13, filt=True, sigma=1.5)
#    features = feature_by_pixel(hyper_image)
    features = preprocessing.robust_scale(features, axis=0)
    pca = decomposition.PCA(n_components=.8,whiten=True)
    features = pca.fit_transform(features)
    
    best, score, all_scores = best_clusters(hyper_image, features, gmm_hyper)
    print best, score
    gmm, gmm_spectra, score = gmm_hyper(hyper_image, features, best)

else:

    features,imgs  = generate_features(hyper_image, peaks, 7, filt=True)
#    features, hypo = feature_by_pixel(hyper_image)
    features = preprocessing.robust_scale(features,axis=0)

#    pca = decomposition.PCA(n_components=2,whiten=True)
#    H = pca.fit_transform(features)
#    comps = pca.components_

    gmm, gmm_spectra, score = kmeans_hyper(hyper_image, features, 3)

plt.figure()
plt.plot(range(2,9), all_scores, 'bo')
plt.ylabel('Calinski-Harabasz Score')
plt.xlabel('Number of Clusters')
plt.show()


colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'black', 'teal']
fig = plt.figure()
plt.imshow(hyper_topo, extent=[0,0.5,0,0.5], cmap='viridis')
plt.colorbar(label='Height (nm)')
plt.show()

fig = plt.figure()
cax = plt.imshow(gmm, cmap=matplotlib.colors.ListedColormap(colors[:len(np.unique(gmm))]), extent=[0,.5,0,.5], interpolation='none')

fig.colorbar(cax,ticks=np.arange(2))
plt.show()

offset = 0.0
plt.figure()

spectra = []
for j,spectrum in enumerate(gmm_spectra):
    spectrum += offset
    plt.plot(wavelengths, spectrum,color=colors[j])
    spectra.append(spectrum)
    offset += .00005
plt.show()

diff = []
difference = 0
labels = []
for i,spectrum1 in enumerate(spectra):
    for j,spectrum2 in enumerate(spectra):
        if i - j >=0:
            continue
        string = str(i)+':'+str(j)
        labels.append(string)
        difference = spectrum1 - spectrum2
        scale = abs(spectrum1).max()
        diff.append(difference/scale)
        
offset = 0   
 
for j,spectrum in enumerate(diff):
    plt.figure() 
    m =  spectrum.max()
#    spectrum += offset
    plt.plot(wavelengths, spectrum, label=labels[j])
    spectra.append(spectrum)
    offset += m
    plt.legend()
    plt.xlabel('Wavenumber (cm^-1)')
    plt.show()
    

