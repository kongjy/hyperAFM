import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter, argrelmax


def get_hypir_peaks(hypir_image, threshold):
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


hypir_data = util.HypirImage('..\\test_data\\Film5_0049.txt')
hypir_image = np.rot90(hypir_data.hypir_image)[::-1,:,:]
topo_image = hypir_data.channel_data[:,:,0]
peaks, spectrum = get_hypir_peaks(hypir_image,.2)

#plt.figure()
#plt.imshow(topo_image, cmap='gnuplot')
#plt.show()
plt.figure()
plt.plot(spectrum)
plt.plot(peaks, spectrum[peaks], 'ro')
plt.show()

im_number=0
fig, axs = plt.subplots(nrows=2,ncols=5)
for i in range(2):
    for j in range(5):
        axs[i,j].imshow(sum_around_peak(hypir_image, peaks[im_number], 25), cmap='cubehelix')
        im_number+=1
plt.show()
