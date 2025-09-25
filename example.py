import numpy as np
from colour import SpectralDistribution
from comps import *


def create_sd(wavelengths, values, name):
    return SpectralDistribution(dict(zip(wavelengths, values)), name=name)


def main():
    wavelengths_nm = np.arange(380, 740, 10)
    wavelengths_m = np.arange(380e-9, 740e-9, 10e-9)
    light = np.ones(wavelengths_m.shape)
    light_sd = dict(zip(wavelengths_m, light))
    light_mod = Light(light_sd)
    generator = Polarizer()
    analyzator = Polarizer().set_angle(0)
    bopp1 = Retarder(d=25e-6, delta_n=0.015).set_angle(45)

    setup = Setup()
    setup.add_light(light_mod)
    setup.add_layer(generator)
    setup.add_layer(bopp1)
    setup.add_layer(analyzator)
    result = setup.calc()

    print(create_sd(wavelengths_nm, result, "model").values)


if __name__ == "__main__":
    main()
