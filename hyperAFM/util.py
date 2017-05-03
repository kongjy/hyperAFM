from igor.binarywave import load
from scipy.signal import detrend
from skimage import feature
from skimage import transform
import csv
import numpy as np
import matplotlib.pyplot as plt
import os

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


class HypirImage():
    """
    """
    def __init__(self, path):
        
        
        self.channel_names = []
        full_path = os.path.realpath(path)
        directory = os.path.dirname(full_path)
        self.parms, channels =  read_anfatec_params(full_path)
    
        self.wavelength_data = np.loadtxt(os.path.join(directory,channels[0]['FileNameWavelengths']))
        
        x_pixel = int(self.parms['xPixel'])
        y_pixel = int(self.parms['yPixel'])
        
        wavenumber_length = self.wavelength_data.shape[0]
    
        image_shape = (x_pixel,y_pixel,wavenumber_length)
            
        hypir_image = np.zeros(image_shape)
        
        pifm_scaling = float(channels[0]['Scale'])
        data = np.fromfile(os.path.join(directory,channels[0]['FileName']),dtype=int)
        print data.shape
        for i,line in enumerate(np.split(data,256)):
            for j, pixel in enumerate(np.split(line,256)):
                    hypir_image[j,i] = pifm_scaling*pixel
                    
        channel_data = np.zeros((x_pixel, y_pixel, len(channels[1:])))
    
        for i, channel in enumerate(channels[1:]):
            
            self.channel_names.append(channel['Caption'])
            data = np.fromfile(os.path.join(directory,channel['FileName']),dtype=int)
            scaling = float(channel['Scale'])
            
            for i,line in enumerate(np.split(data,256)):
                for j, pixel in enumerate(np.split(line,256)):
                        channel_data[j,i,:] = (scaling*pixel)

        self.hypir_image = hypir_image
        self.channel_data = channel_data



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



def read_anfatec_params(path):
    """
    Reads in an ANFATEC parameter file. This file is produced by the Molecular
    Vista PiFM system and describes all parameters need to interpret the data 
    files produced when the data is saved.
    
    Input:
        path: a path to the ANFATEC parameter file.
        
    Output:
        file_descriptions: A list of dictionaries, with each item in the list 
            corresponding to a channel that was recorded by the PiFM.
        scan_params: A dictionary of non-channel specific scan parameters.
        
    """
    
    file_descriptions = []
    scan_params = {}
    parameters = {}
    inside_description = False

    with open(path,  'r') as csvfile:
        reader = csv.reader(csvfile,delimiter='\t')
        for i,row in enumerate(reader): 
            
            if row:
                
                # First line of the file is useless. We tell the reader to stop at ';'
                if row[0] ==';ANFATEC Parameterfile':
                    continue
                if row[0][0] == ';':
                    break
                
                # This string indicates that we have reached a channel description.
                if row[0].endswith('Begin'):
                    inside_description = True
                    continue
                   
                # Here we handle the unicode characters and form our key value pairs
                new_row =  row[0].replace(' ','')
                split_row = new_row.split(':')
                split_row[-1] = split_row[-1].decode('unicode-escape')  
                
                # We want to save the channel parameters to a separate structure.
                if inside_description:
                    parameters[split_row[0]] = split_row[-1]
                else:
                    scan_params[split_row[0]] = split_row[-1]
                
                if row[0].endswith('End'):
                    del parameters[row[0]]
                    file_descriptions.append(parameters)
                    parameters = {}
                    inside_description = False
                    
        csvfile.close()
    
    return scan_params, file_descriptions

def load_hypir_numpy(folder_path):
    """
    Loads a hypir image that has previously been saved into a numpy format.
    """
    files = os.listdir(folder_path)
    image_list = []
    
    for i, file_name in enumerate(files):
        path = os.path.join(folder_path, file_name)
        image_list.append(np.load(path))
        
    return np.column_stack(tuple(image_list))
