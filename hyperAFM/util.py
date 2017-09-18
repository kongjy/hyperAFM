from igor.binarywave import load
from scipy.signal import detrend
from skimage import feature
from skimage import transform
import io
import numpy as np
import pandas as pd
import h5py
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
        
    data = np.rot90(data)    
    return data

def hyperslice(hyper, start, stop, rows = None , cols = None):
    """
    Sums a range of wavenumbers within a hyperspectral image. 
    
    Paramters 
    ----------
        hyper: class from HyperImage
        start: int
            start wavenumber
        stop: int
            stop wavenumber
        rows: tuple, (start, stop)
    	    starting and ending indices for rows within image 
            be displayed. If all rows are desired, can 
            leave blank.  
        cols: tuple
            same as above, but for columns. 
    Returns
    -------
        slc: ndarray
            sum of intensities between the specified start and
            stop wavenumbers 
        
    """
    #show entire hyper image if no tuples are passed into arguments
    if rows == None: 
        rows = (0,hyper.channel_data.shape[0])
    if cols == None:
        cols = (0, hyper.channel_data.shape[1])        

    wavenumber = hyper.wavelength_data.tolist()
    wavenumberlist = [int(x) for x in wavenumber]
    #flip start and stop indices because of the 
    #way the wavenumber data is stored. 
    start_index = wavenumberlist.index(stop)
    stop_index = wavenumberlist.index(start) 
    span = stop_index - start_index
    slc = hyper.hyper_image[rows[0]:rows[1],cols[0]:cols[1],start_index]
    for i in range(span):
        slc += hyper.hyper_image[rows[0]:rows[1],cols[0]:cols[1],start_index+i]
    
    return slc
    
    

class HyperImage():
    """
    A class representing a Hyper image. Give the path to the Hyper data, and 
    receive a class that stores this information as a hyper image, and series 
    of channel images.
    """
    def __init__(self, path):
        
        self.wavelength_data = None
        self.channel_names = []
        full_path = os.path.realpath(path)
        directory = os.path.dirname(full_path)
        
        # Get the scan parameters and channel details.
        self.parms, channels, e =  read_anfatec_params(full_path)
        
        x_pixel = int(self.parms['xPixel'])
        y_pixel = int(self.parms['yPixel'])
        
        self.wavelength_data = np.loadtxt(os.path.join(directory,str(channels[0]['FileNameWavelengths'])))
        wavenumber_length = self.wavelength_data.shape[0] 
        image_shape = (x_pixel,y_pixel,wavenumber_length)

        hyper_image = np.zeros(image_shape)
        
        # This scales the integer data into floats.
        pifm_scaling = float(channels[0]['Scale'])
        
        # Read the Raw Hyper data from the bitfile.
        data = np.fromfile(os.path.join(directory,channels[0]['FileName']),dtype='i4')
        for i,line in enumerate(np.split(data,y_pixel)):
            for j, pixel in enumerate(np.split(line,x_pixel)):
                    hyper_image[j,i,:] = pifm_scaling*pixel
                    
        # Put all the different channels into one big array.
        channel_data = np.zeros((x_pixel, y_pixel, len(channels[1:])))
        for ch, channel in enumerate(channels[1:]):
            self.channel_names.append(channel['Caption'])
            data = np.fromfile(os.path.join(directory,channel['FileName']),dtype='i4')
            scaling = float(channel['Scale'])

            for i,line in enumerate(np.split(data,y_pixel)):
                for j, pixel in enumerate(np.split(line,x_pixel)):
                        channel_data[j,i,ch] = (scaling*pixel)

        # Here's how we access the different hyper and channel data.
        self.hyper_image = np.rot90(hyper_image, k=-1)
        self.channel_data = np.rot90(channel_data, k=-1)
        
        self.hyper_image = self.hyper_image[:,::-1,:]
        self.channel_data = self.channel_data[:,::-1,:]
        

#
#class PiFMImage():
#    """
#    A class representing a Hyper image. Give the path to the Hyper data, and receive a class that 
#    stores this information as a hyper image, and series of channel images.
#    """
#    def __init__(self, path):
#        
#        self.wavelength_data = None
#        self.channel_names = []
#        full_path = os.path.realpath(path)
#        directory = os.path.dirname(full_path)
#        
#        # Get the scan parameters and channel details.
#        self.parms, channels =  read_anfatec_params(full_path)
#        
#        x_pixel = int(self.parms['xPixel'])
#        y_pixel = int(self.parms['yPixel'])
#
#        # Put all the different channels into one big array.
#        channel_data = np.zeros((x_pixel, y_pixel, len(channels)))
#        for ch, channel in enumerate(channels):
#            self.channel_names.append(channel['Caption'])
#            data = np.fromfile(os.path.join(directory,channel['FileName']),dtype='i4')
#            scaling = float(channel['Scale'])
#
#            for i,line in enumerate(np.split(data,y_pixel)):
#                for j, pixel in enumerate(np.split(line,x_pixel)):
#                        channel_data[j,i,ch] = (scaling*pixel)
#
#        # Here's how we access the different hyper and channel data.
#        self.channel_data = np.rot90(channel_data, k=-1)


#def align_images(master_data, target_data):
#    """
#    Given a master image, this function aligns the target image to this master 
#    data.
#    
#    What format(s) do master and target data have to be in? 
#    
#    """
#    target_shifted = target_data.copy()
#    master_topo = master_data[:,:,0]
#    target_topo = target_data[:,:,0]
#
#    # Get the shift using phase correlation.
#    shift,e,b = feature.register_translation(master_topo, target_topo)
#
#    # Shift the data.
#    tform = transform.SimilarityTransform(translation=[-shift[1],shift[0]])
#    
#    for i in range(target_shifted.shape[2]):
#        target_shifted[:,:,i] = transform.warp(target_shifted[:,:,i], tform, preserve_range=True)
#    
#    return target_shifted
class PiFMImage():
    """
    A class representing a PiFM image. Give the path to the PiFM data
    and receive a class that stores this information as a hyper image, 
    and series of channel images.
    
    Input: 
        path: Path to ANFATEC parameter file. This is the text file that
        is generated with each scan.
        
    Attributes: 
        channel_names: list of all data channels in channel_data 
        channel_data: a resolution x resolution x no. channel array. 
                    channel_data[:,:,0] will return the matrix 
                    corresponding to the channel in channel_names[0]
        parms: a dictionary of all scan parameters 
        spectra_files: list of filenames containing point spectra 
        point_spectra: list of df containing point spectra associated 
                        with scan. point_spectra[0] will return the df
                        corresponding to the file in spectra_file[0]
                    
    """
    def __init__(self, path):
        
        
        self.channel_names = []
        self.spectra_files = []
        full_path = os.path.realpath(path)
        directory = os.path.dirname(full_path)
        
        # Get the scan parameters and channel details.
        self.parms, channels, spectra =  read_anfatec_params(full_path)
       
        x_pixel = int(self.parms['xPixel'])
        y_pixel = int(self.parms['yPixel'])
        
        #Make one big array for all the data channels.
        channel_data = np.zeros((x_pixel, y_pixel, len(channels)))
        for i, channel in enumerate(channels):
            
            self.channel_names.append(channel['Caption'])
            data = np.fromfile(os.path.join(directory,channel['FileName']),\
                               dtype='i4')
            #scaling = float(channel['Scale'])
            channel_data[:,:,i] = np.reshape(data, (256,256))
            
            #for i,line in enumerate(np.split(data,y_pixel)):
            #    for j, pixel in enumerate(np.split(line,x_pixel)):
            #            channel_data[j,i,:] = (scaling*pixel)
        point_spectra = []
        for i in range(len(spectra)):
            self.spectra_files.append(spectra[i]['FileName'])
            data = pd.read_csv(os.path.join(directory,spectra[i]['FileName']),\
                               delimiter = '\t')
            data.columns = ['wavenumber' , 'intensity']
            point_spectra.append(data)
        
        
        # Here's how we access the different hyper and channel data.
        self.channel_data = channel_data
        self.point_spectra = point_spectra

def align_images(image, offset_image):
    
    """
    Flattens, aligns and crops two images to a common area. Retains original size by 
    padding cropped area with zeros. 
    
    Input: 
        image: any data channel
        offset_image: same data channel of a different scan. 
        
    Output: 
        ref_imagepadded, offset_image
    """
    #flatten images
    image = detrend(image, axis=1, type = "linear")
    offset_image = detrend(offset_image, axis=1, type = "linear")
    
    #find shift, error, and phase difference between the two images
    shift, error, diffphase = feature.register_translation(image, offset_image)
    
    #shift the offset image
    offset_imagecrop = offset_image[:-int(shift[0]),-int(shift[1]):]
    offset_imagepadded = np.zeros((256,256))
    offset_imagepadded[:offset_imagecrop.shape[0], \
                       :offset_imagecrop.shape[1]] = offset_imagecrop
    
    #swap the reference and offset image. take offset_image as the new ref. 
    newref_image = offset_imagepadded 
    offset_image = image
    
    #detect pixel shift again
    shift1, error1, diffphase1 = feature.register_translation(newref_image, offset_image)
    
    #shift original reference image to match offset image
    ref_imagecrop = offset_image[-int(shift1[0]):, :]
    ref_imagepadded = np.zeros((256,256))
    ref_imagepadded[:ref_imagecrop.shape[0], :ref_imagecrop.shape[1]] = ref_imagecrop
    

    return ref_imagepadded, offset_imagepadded
    
    

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
    spectra_descriptions = []
    scan_params = {}
    parameters = {}
    inside_description = False


    with io.open(path,  'r', encoding = "ISO-8859-1") as f:
        
        for i,row in enumerate(f): 
            
            # Get rid of newline characters at the end of the line.
            row = row.strip()
            #check to make sure its  not empty 
            if row:
                # First line of the file is useless. We tell the reader to stop at ';'
                if row[0] == unicode(';'):
                    continue
                
                # This string indicates that we have reached a channel description.
                if row.endswith('Begin') & row.startswith('File'):
                    inside_description = True
                    continue
                if row.endswith('SpectrumDescBegin'):
                    inside_description = True
                    continue
                if row.endswith('End') & row.startswith('File'):
                    file_descriptions.append(parameters)
                    parameters = {}
                    inside_description = False
                if row.endswith('SpectrumDescEnd'):
                    spectra_descriptions.append(parameters)
                    parameters = {}
 
                #split between :; creates list of two elements 
                split_row = row.split(':')
                
                for i, el in enumerate(split_row):
                    split_row[i] = el.strip()
                
                # We want to save the channel parameters to a separate structure.
                if inside_description:
                    parameters[split_row[0]] = split_row[-1]
                else:
                    scan_params[split_row[0]] = split_row[-1]
            
                    
    return scan_params, file_descriptions, spectra_descriptions


def load_hyper_numpy(folder_path):
    """
    Loads a hyper image that has previously been saved into a numpy format.
    INPUT: Folder containing each line of a hyperspectral image, which are 
    in .npy format. 
    
    OUTPUT: Three dimensional numpy array with the first two dimensions
    corresponding to x, y space and the third to the IR spectra obtained. 
    The third number indicates how many data points there are in 
    a spectrum, but does not contain information about the wavenumber. 
    **For our datasets only: the spectra were taken from 760 to 1875 cm-1
    with a 5 cm-1 spacing. 
    """
    files = os.listdir(folder_path)
    image_list = []
    
    for i, file_name in enumerate(files):
        path = os.path.join(folder_path, file_name)
        image_list.append(np.load(path))
        
    return np.column_stack(tuple(image_list))


def hyper_to_hdf5(path, dest_path):
    """
    Convert a series of MolecularVista files into hdf5 format.
    
    Input:
        path- The path to the Anfatec Parameter file that contains references to
        all necessary data.
        
        dest_path- desired path for the hdf5 file.
    Output:
        Saves a .hdf5 file to the dest_path path. 
    """
    name = os.path.basename(path)
    base, ext = os.path.splitext(name)
    new_name = base + '_HDF5'+'.hdf5'
    
    hyper_data= HyperImage(path)
    hyper_image = hyper_data.hyper_image
    
    channel_data = hyper_data.channel_data
    channel_names = hyper_data.channel_names
    
    h5f = h5py.File(os.path.join(dest_path, new_name))
    
    h5f.create_dataset('hyper_image',data=hyper_image)
    
    for i,channel_name in enumerate(channel_names):
        h5f.create_dataset(channel_name, data=channel_data[:,:,i])
        
    h5f.close()
    
    return


def hyper_from_hdf5(path):
    """
    Loads Hyperspectral data from a hdf5 file.
    """
    
    h5f = h5py.File(path,mode='r')
    
    hyper_image = h5f['hyper_image']
    channel_data = h5f['channel_data']
    
    h5f.close()
    
    return hyper_image, channel_data
    
