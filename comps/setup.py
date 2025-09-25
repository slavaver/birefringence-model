import numpy as np

from comps import Polarizer, Retarder, ColorFilter

class Setup:
    def __init__(self):
        self.layers = []
        self.light = None

    def add_light(self, light):
        self.light = light

    def add_layer(self, layer):
        self.layers.append(layer)


    def _calc(self, wavelength, light_vector):
        intermediate = None
        for layer in self.layers:
            if intermediate is None:
                intermediate = np.dot(layer.get_matrix(wavelength), light_vector)
            if isinstance(layer, Polarizer):
                intermediate = np.dot(layer.get_matrix(wavelength), intermediate)
            elif isinstance(layer, Retarder):
                intermediate = np.dot(layer.get_matrix(wavelength), intermediate)
            elif isinstance(layer, ColorFilter):
                intermediate = np.dot(layer.get_matrix(wavelength), intermediate)
        return intermediate


    def calc(self):
        result = np.array([])
        for wavelength, vector in self.light.get_stokes_vectors().items():
            result = np.append(result, np.real(self._calc(wavelength, vector)[0, 0]))
        return result