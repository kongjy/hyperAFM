import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter, argrelmax



hypir_data = util.HypirImage('..\\test_data\\Film5_0049.txt')
hypir_image = hypir_data.hypir_image

im_list = []
for i in range(256):
    for j in range(256):
        im_list.append(hypir_image[i,j,:])
    break

spectrum = np.column_stack(tuple(im_list)).mean(axis=-1)


#spec = medfilt(spectrum, 5)  # Still some noise, get rid of them.
spec = savgol_filter(spectrum, 11, 1, 1,mode='constant')  # First derivative.

pos_spec = spec.copy()
neg_spec = -spec.copy()



def get_thresh(fraction_thresh, spec_deriv):
    return fraction_thresh*spec_deriv.max()


threshold = get_thresh(.1, pos_spec)
pos_spec[pos_spec < threshold] = 0
threshold = get_thresh(.1, neg_spec)
neg_spec[neg_spec < threshold] = 0

plt.plot(spec)

pos_peaks_list = argrelmax(pos_spec, order=7)
neg_peaks_list = argrelmax(neg_spec, order=7)

plt.plot(pos_peaks_list[0], spec[pos_peaks_list[0]], 'ro')
plt.plot(neg_peaks_list[0], spec[neg_peaks_list[0]], 'go')