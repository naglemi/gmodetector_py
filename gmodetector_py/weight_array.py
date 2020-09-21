from gmodetector_py import regress
import numpy as np
from scipy import sparse
import pandas as pd
from gmodetector_py import find_desired_channel
from gmodetector_py import slice_desired_channel
from gmodetector_py import CLS_to_image

class WeightArray:
    """A 3D array containing weights for each spectral component, obtained by regression of hybercube onto design matrix

    :param test_matrix: An object of class XMatrix (containing normalized spectra for each known component, and intercept if applicable)
    :param test_cube: An object of class Hypercube (containing spectra for each pixel)
    :ivar wavelengths: contains the contents of ``wavelengths`` passed from ``test_matrix`` and ``test_cube`` (must be same, or will yield error)
    :ivar weights: 3D array containing weight values
    :ivar components: A list of spectral components (including intercept if applicable) – contains the contents of ``fluorophore_ID_vector`` passed through``test_matrix.components``

    """

    def save(self, path):
        for i in range(0, len(self.components)):
            if i == 0:
                array_in_coordinate = pd.DataFrame(sparse.coo_matrix(self.weights[:, :, i]))
            if i > 0:
                matrix_slice_in_triplet = pd.DataFrame(sparse.coo_matrix(self.weights[:, :, i]))
                array_in_coordinate = pd.concat([array_in_coordinate, matrix_slice_in_triplet[:, 2]],
                axis = 1)
                print('array shape is...')
                print(array_in_coordinate.shape)
                print('head row of array is...')
                print(array_in_coordinate[:1])
        array_in_coordinate = pd.DataFrame(array_in_coordinate,
        columns = ['rows', 'cols'] + self.components)
        array_in_coordinate.to_csv(path)

    def plot(self, desired_component, color, cap):
        """Plot a single channel selected from a weight array produced by regression

                :param desired_component: A string matching the ID of the component to be plotted (e.g. 'GFP')
                :param color: A string equal to 'red', 'blue', or 'green' – the color that the extracted band will be plotted in
                :param cap: A numeric value of the spectral intensity value that will have maximum brightness in the plot. All with greater intensity will have the same level of brightness. Think of this as image exposure on a camera.

        """
        index_of_desired_channel = find_desired_channel(self.components,
                                                        desired_component)
        Weights_desired_peak_channel = slice_desired_channel(self.weights,
                                                             index_of_desired_channel)
        plot_out = CLS_to_image(CLS_matrix = Weights_desired_peak_channel,
                                cap = cap, mode = 'opaque',
                                match_size=False, color=color)
        return(plot_out)

    def __init__(self, test_matrix, test_cube):

        if test_matrix.wavelengths.astype(np.float).all() != test_cube.wavelengths.astype(np.float).all():
            raise Exception("Design matrix and hypercube do not have the same ``wavelengths`` attribute. Make sure to set the same ``min_desired_wavelength`` and ``max_desired_wavelength`` when creating both objects.")

        self.wavelengths = test_matrix.wavelengths
        self.weights = regress(test_matrix = test_matrix,
                               test_cube = test_cube)
        self.components = test_matrix.components
        self.source = test_cube.source
