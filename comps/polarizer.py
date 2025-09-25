from sympy import symbols, pi, matrix2numpy
from sympy.physics.optics.polarization import mueller_matrix, linear_polarizer

class Polarizer:
    def __init__(self):
        self.angle = 0
        self.cache = None

    def set_angle(self, angle):
        self.angle = angle
        self.cache = None
        return self

    def get_matrix(self, wavelength):
        if self.cache is None:
            theta_p = symbols("theta_p", real=True)
            matrix = mueller_matrix(linear_polarizer(theta_p)).subs({theta_p: self.angle * (pi / 180)})
            self.cache = matrix2numpy(matrix, dtype=float)
        return self.cache