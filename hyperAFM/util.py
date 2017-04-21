from igor.binarywave import load
import os
import matplotlib.pyplot as plt
from scipy.signal import detrend

def load_ibw(path, flatten=True):
    """
    Given a path to an Igor Binary Wave, return the image file as a 3 dimensional 
    numpy array.
    
    Input:
        path: string file path to .ibw file
        flatten (optional): boolean input to flatten topography data.
    Output:
        data: 3 dimensional numpy array containing .ibw data.
    """
    data = load(path)['wave']['wData']

    # Flatten the topography data by extracting any linear response.
    if flatten == True:   
        flat_topo = data.copy()
        flat_topo[:, :, 0] = detrend(flat_topo[:, :, 0])
        data = flat_topo
        
    return data

path = 'DIRECT\\SKPMcAFM_set1\\'
file_list = os.listdir(path)


data = load_ibw(path+file_list[1], flatten=True)

plt.figure()
plt.imshow(data[:,:,0])
plt.show()