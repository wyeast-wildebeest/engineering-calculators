import numpy as np
from scipy.optimize import fsolve


class Fluid:
    def __init__(self, name, density, dynamic_viscosity, temperature):
        self.name = name
        self.density = density
        self.dynamic_viscosity = dynamic_viscosity
        self.temperature = temperature


class PipeCircular:
    def __init__(self, diameter, length, roughness):
        self.diameter = diameter
        self.length = length
        self.roughness = roughness
        self.cross_sectional_area = circular_area(diameter)
        self.wetted_perimeter = circular_perimeter(diameter)
        self.hydraulic_diameter = hydraulic_dia(perimeter=self.wetted_perimeter, area=self.cross_sectional_area)
        self.velocity = None
        self.reynolds_number = None
        self.friction_factor = None
        self.dp = None

    def calc_velocity(self, flow_rate):
        self.velocity = flow_rate / self.cross_sectional_area

    def calc_reynolds(self, fluid):
        self.reynolds_number = reynolds(density=fluid.density,
                                        hydraulic_diameter=self.hydraulic_diameter,
                                        velocity=self.velocity,
                                        dynamic_viscosity=fluid.dynamic_viscosity
                                        )

    def calc_dp_friction(self, fluid):
        self.friction_factor = friction_factor_colebrook(pipe=self, reynolds_number=self.reynolds_number)
        self.dp = dp_friction(friction_factor=self.friction_factor, fluid=fluid, pipe=self, velocity=self.velocity)


def friction_factor_colebrook(pipe, reynolds_number, f_guess=0.04):
    """Returns the Darcy friction factor using the Colebrook-White equation"""

    f_guess = np.array(f_guess)
    roughness = pipe.roughness
    hydraulic_diameter = pipe.hydraulic_diameter

    a = 2.51 / reynolds_number
    b = roughness / 3.7 / hydraulic_diameter

    def colebrook(f):
        return -1/np.sqrt(f) - 2 * np.log10(a * 1/np.sqrt(f) + b)

    return fsolve(colebrook, f_guess)[0]


def reynolds(density, hydraulic_diameter, velocity, dynamic_viscosity):
    """Returns reynolds number of flow"""

    return density * hydraulic_diameter * velocity / dynamic_viscosity


def dp_friction(friction_factor, fluid, pipe, velocity):
    """Returns pressure drop due to frictional losses using Darcy-Weisbach"""

    length = pipe.length
    hydraulic_diameter = pipe.hydraulic_diameter
    density = fluid.density

    return length * friction_factor * density * velocity**2 / 2 / hydraulic_diameter


def hydraulic_dia(perimeter, area):
    """Returns hydraulic diameter given perimeter and area"""

    return 4 * area / perimeter


def circular_area(diameter):
    """Returns area of a circle given it's diameter"""

    return np.pi * diameter**2 / 4


def circular_perimeter(diameter):
    """Return the perimeter of a circle given the diameter"""

    return np.pi * diameter
