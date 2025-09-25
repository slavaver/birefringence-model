from sympy import symbols, matrix2numpy
from sympy.physics.optics.polarization import stokes_vector

class Light:
    def __init__(self, light_sd):
        """
        light_sd: {wavelength: I, wavelength: I,...}
        """
        self.light_sd = light_sd
        self.cache = None

    def _create_unpolarized_light(self, intensity = 1):
        I = symbols("I", real=True)
        vector = stokes_vector(0, 0, 0, I).subs({I: intensity})
        return matrix2numpy(vector, dtype=float)
    
    def get_stokes_vectors(self):
        if self.cache is None:
            result = {}
            for wavelength in self.light_sd:
                result[wavelength] = self._create_unpolarized_light(self.light_sd[wavelength])
            self.cache = result
        return self.cache