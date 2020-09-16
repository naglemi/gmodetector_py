from gmodetector_py import regress
import numpy as np

class WeightArray:
    """A 3D array containing weights for each spectral component, obtained by regression of hybercube onto design matrix

    :param test_matrix: An object of class XMatrix (containing normalized spectra for each known component, and intercept if applicable)
    :param test_cube: An object of class Hypercube (containing spectra for each pixel)
    :ivar wavelengths: contains the contents of ``wavelengths`` passed from ``test_matrix`` and ``test_cube`` (must be same, or will yield error)
    :ivar weights: 3D array containing weight values
    :ivar components: A list of spectral components (including intercept if applicable) – contains the contents of ``fluorophore_ID_vector`` passed through``test_matrix.components``

    """

    def plot(self, desired_wavelength, color, cap):
        index_of_desired_channel = find_desired_channel(self.components,
                                                        desired_wavelength)
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
