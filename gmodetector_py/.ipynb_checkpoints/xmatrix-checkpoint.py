class XMatrix:
    """A design matrix for multiple linear regression, with effect and observation labels
    
    :param value: value to set as the ``attribute`` attribute
    :ivar attribute: contains the contents of ``values`` passed as init
    
    """
    #i = 12345

    def _nan_to_zero(self):
        return(np.nan_to_num(self.matrix))
    
    def _plot(self, tick_step = np.int(50)):
        # style
        plt.style.use('seaborn-darkgrid')

        # create a color palette
        palette = plt.get_cmap('Set1')

        # multiple line plot
        num=0

        XMatrix_plottable = pd.DataFrame(self.matrix)

        for column in XMatrix_plottable:
            num+=1 
            plt.plot(self.wavelengths,
                     XMatrix_plottable[column],
                     marker='',
                     color=palette(num),
                     linewidth=1, alpha=0.9,
                     label=column)

        # Add legend
        plt.legend(loc=2, ncol=2)
        print("HEY")
        print(self.wavelengths.shape[0]-1)
        print(len(self.wavelengths))
        
        # Change tick marks
        #plt.xticks(np.arange(start = float(min(self.wavelengths)),
        #                     stop = float(max(self.wavelengths)),
        #                     step = tick_step))
        

        # Add titles
        plt.title("Design matrix of spectral components", loc='left', fontsize=12, fontweight=0, color='orange')
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Signal intensity (normalized)")
    
    def __init__(self, fluorophore_ID_vector, spectral_library_path,
                 intercept, wavelengths,
                 min_desired_wavelength, max_desired_wavelength):
        # Define attribute with contents of the value param
        
        if intercept == 1:
            components = fluorophore_ID_vector.copy()
            components.insert(0, "Intercept")
        
        self.matrix = build_X(fluorophore_ID_vector = fluorophore_ID_vector,
                                             spectral_library_path = spectral_library_path,
                                             intercept = intercept,
                                             wavelengths = wavelengths,
                                             min_desired_wavelength = min_desired_wavelength,
                                             max_desired_wavelength = max_desired_wavelength)
        self.wavelengths = np.asarray(wavelengths)[find_desired_indices(wavelengths,
                                                            min_desired_wavelength,
                                                            max_desired_wavelength)] 
        self.components = components