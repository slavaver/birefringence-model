import numpy as np

class ColorFilter:

    def __init__(self, sd):
        self.sd = sd

    def get_matrix(self, wavelength):
        return np.identity(4) * np.interp(wavelength, np.arange(380e-9, 740e-9, 10e-9), list(self.sd.values()))