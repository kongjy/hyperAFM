import numpy as np
import util
from gen_features import generate_features, get_hyper_peaks
from sklearn.feature_selection import VarianceThreshold
import os
import matplotlib.pyplot as plt

path = os.path.abspath('C:/Users/jarrison/Documents/Ion trEFM paper/20170702 PEDOT PiFM/40mg_EG_0002.txt')


hyp = util.HyperImage(path)

hyper_image = hyp.hyper_image
channel_data = hyp.channel_data
wavelengths = hyp.wavelength_data

peaks, avg_spectrum = get_hyper_peaks(hyper_image, .05)

plt.figure()
plt.plot(wavelengths, avg_spectrum)
plt.plot(wavelengths[peaks], avg_spectrum[peaks], 'bo')
plt.show()

features, imgs = generate_features(hyper_image, peaks, 5, filt=True)


threshold = 0.0
kbest = VarianceThreshold(threshold=threshold)

X = kbest.fit_transform(features)
variances = kbest.variances_

plt.figure()
plt.plot(wavelengths[peaks], variances, '.')
plt.show()
