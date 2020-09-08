from gmodetector_py import XMatrix


def test_XMatrix():
    wavelengths = read_wavelengths('tests/example.hdr')
    test_matrix = XMatrix(fluorophore_ID_vector = ['DsRed', 'ZsYellow', 'Chl', 'Diffraction'],
                          spectral_library_path = 'spectral_library/',
                          intercept = 1,
                          wavelengths = wavelengths
                          min_desired_wavelength = 550,
                          max_desired_wavelength = 600)
    
    assert len(test_matrix.wavelengths) == test_matrix.matrix.shape[0]
