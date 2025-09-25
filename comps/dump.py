from functools import partial

import numpy as np
from sympy import symbols, pi, matrix2numpy
from sympy.physics.optics.polarization import stokes_vector, mueller_matrix, linear_polarizer, phase_retarder

def create_unpolarized_light(intensity = 1):
    I = symbols("I", real=True)
    vector = stokes_vector(0, 0, 0, I).subs({I: intensity})
    return matrix2numpy(vector, dtype=float)

def create_polarizer(angle):
    theta_p = symbols("theta_p", real=True)
    matrix = mueller_matrix(linear_polarizer(theta_p)).subs({theta_p: angle * (pi / 180)})
    return matrix2numpy(matrix, dtype=float)

def create_retarder():

    '''
    theta : The angle of the fast axis relative to the horizontal plane.
    delta : The phase difference between the fast and slow axes of the transmitted light.
    '''

    theta_r, delta_r = symbols("theta_r, delta_r", real=True)
    return mueller_matrix(phase_retarder(theta_r, delta_r)), theta_r, delta_r

def retarder2numpy(retarder, delta, angle):
    r, t, d = retarder
    matrix = r.subs({d: delta, t: angle * (pi / 180)})
    return matrix2numpy(matrix, dtype=complex)

def retardace(delta_n, d, wavelength):
    return 2 * np.pi * delta_n * d / wavelength

bopp_retardace = partial(retardace, 0.0191, 25e-6)

light_sd = np.ones((36, )) * 10
wavelengths = np.arange(380e-9, 740e-9, 10e-9)

np_bopp_retardace = bopp_retardace(wavelengths)


generator = create_polarizer(0)
analyzator = create_polarizer(0)
retarder = create_retarder()

result = np.array([])

for I, r in zip(light_sd, np_bopp_retardace):
    light = create_unpolarized_light(I)
    np_retarder = retarder2numpy(retarder, r, 45)
    light_pol = np.dot(generator, light)
    light_ret = np.dot(np_retarder, light_pol)
    light_out = np.dot(analyzator, light_ret)
    result = np.append(result, np.real(light_out[0, 0]))    



## FIXING LIGHT
fix_wavelengths = np.arange(380, 740, 10)
# fix_sd = [14.2895333333333, 23.9451333333333, 44.6433, 64.7786, 74.1088333333333, 77.3498333333333, 78.9719666666667, 80.2351666666667, 81.4834333333333, 82.3317, 82.9640666666667, 83.2877333333333, 83.1908, 82.9297333333333, 82.6524, 81.8469666666667, 80.9427333333333, 80.4515333333333, 79.9989333333333, 79.8377, 79.1865333333333, 79.1557, 79.9651, 80.991, 81.792, 82.2057333333333, 82.6595333333333, 82.9953666666667, 83.2479666666667, 82.4992333333333, 82.5106666666667, 84.2103333333333, 85.8148666666667, 86.3827333333333, 85.4220333333333, 84.0596333333333]
# fix_sd = [1.02150633333333, 1.22108333333333, 4.59990333333333, 9.57323666666667, 12.0412666666667, 13.1547333333333, 13.9052, 14.5054666666667, 15.0513, 15.5412333333333, 15.9737666666667, 16.3061333333333, 16.4937, 16.5734333333333, 16.5796666666667, 16.4207, 16.1971, 16.0239, 15.8668333333333, 15.7942, 15.6502666666667, 15.6510333333333, 15.8345, 16.0804666666667, 16.3029, 16.4753, 16.6792, 16.8821666666667, 17.0981333333333, 17.1339333333333, 17.3388666666667, 17.8801, 18.4261333333333, 18.7574333333333, 18.6731, 18.4516666666667]
# fix_sd = [0.981260333333333, 1.04508366666667, 2.43083666666667, 5.19996, 6.88642, 7.78318666666667, 8.43209333333333, 9.00913, 9.52753, 10.03198, 10.4946333333333, 10.8758666666667, 11.1299333333333, 11.2575666666667, 11.3121666666667, 11.2161666666667, 11.0483, 10.8964333333333, 10.7566666666667, 10.6828666666667, 10.5792, 10.5844666666667, 10.733, 10.9442666666667, 11.1459, 11.3316333333333, 11.5623666666667, 11.7947, 12.0592, 12.2187666666667, 12.5109333333333, 13.0386, 13.5807666666667, 13.9591, 13.9556, 13.8487666666667]
fix_sd = [0.742619666666667, 0.799139333333333, 1.09863233333333, 1.37901666666667, 1.44836666666667, 1.45682, 1.44903, 1.42270333333333, 1.40605333333333, 1.39094, 1.37492333333333, 1.35868, 1.33419666666667, 1.30908333333333, 1.28330666666667, 1.25242666666667, 1.22265, 1.18907666666667, 1.15656, 1.12976333333333, 1.10291333333333, 1.08193, 1.06385333333333, 1.047288, 1.02883866666667, 1.012947, 0.998496666666667, 0.982877, 0.974313666666667, 0.961759333333333, 0.95051, 0.939776333333333, 0.934979666666667, 0.926681, 0.917792, 0.942096]
fix_SD = create_sd(fix_wavelengths, fix_sd, "light")
from colour import SpectralShape

plot_sds([
fix_SD.trim(SpectralShape(440, 730, 10)).align(SpectralShape(380, 730, 10), extrapolator_kwargs={"method": "Constant"})
# fix_SD
])
def get_string_to_copy(sd):
    data = sd.values
    list_of_strings = [str(x) for x in data]
    print("\t".join(list_of_strings))

get_string_to_copy(fix_SD.trim(SpectralShape(440, 730, 10)).align(SpectralShape(380, 730, 10), extrapolator_kwargs={"method": "Constant"}))

## Normalization
filtered = df[(df["Поляризаторы"] == "без") & (df["Краска"] == "без")]
wave_cols = [i for i in range(380, 731, 10)]
overall_max = filtered[wave_cols].to_numpy().max()
df.loc[:, wave_cols] = df[wave_cols] / overall_max