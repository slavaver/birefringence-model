from math import pi

from sympy import symbols, matrix2numpy
from sympy.physics.optics.polarization import mueller_matrix, phase_retarder

class Retarder:

    def __init__(self, d=0, delta_n=0):
        self.angle = 0
        self.d = d
        self.delta_n = delta_n
        self.cache = None

    def set_angle(self, angle=45):
        self.angle = angle
        self.cache = None
        return self
    
    def _retardace(self, wavelength):
        return 2 * pi * self.delta_n * self.d / wavelength

    def get_matrix(self, wavelength):
        '''
        theta : The angle of the fast axis relative to the horizontal plane.
        delta : The phase difference between the fast and slow axes of the transmitted light.
        '''
        if self.cache is None:
            self.theta_r, self.delta_r = symbols('theta_r, delta_r', real=True)
            matrix = mueller_matrix(phase_retarder(self.theta_r, self.delta_r))
            self.cache = matrix.subs({self.theta_r: self.angle * (pi / 180)})
        return matrix2numpy(self.cache.subs({self.delta_r: self._retardace(wavelength)}), dtype=complex)