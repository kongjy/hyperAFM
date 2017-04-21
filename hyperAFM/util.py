from igor.binarywave import load
from scipy.signal import detrend
from skimage import feature
from skimage import transform

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


def load_hypir(path):
    """
    """
    
    
    
    
    return


def align_images(master_data, target_data):
    """
    Given a master image, this function aligns the target image to this master 
    data.
    
    """
    target_shifted = target_data.copy()
    master_topo = master_data[:,:,0]
    target_topo = target_data[:,:,0]

    # Get the shift using phase correlation.
    shift,e,b = feature.register_translation(master_topo, target_topo)
    
    # Shift the data.
    tform = transform.SimilarityTransform(translation=-shift[::-1])
    
    for i in range(target_shifted.shape[2]):
        target_shifted[:,:,i] = transform.warp(target_shifted[:,:,i], tform, preserve_range=True)
    
    return target_shifted


    
