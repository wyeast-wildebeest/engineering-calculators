import numpy as np
from scipy.optimize import fsolve
import warnings

ACCELERATION_GRAVITY = 9.81  # m/s2


class Fluid:
    """Fluid object"""

    def __init__(self, name, density, dynamic_viscosity, temperature):
        self.name = name
        self.density = density
        self.dynamic_viscosity = dynamic_viscosity
        self.temperature = temperature


class Pipe:
    """Pipe segment for a conduit. Determines geometry from inputs.
    Assumes circular cross-section if diameter is given and rectangular cross-section if width and height are given.
    """

    def __init__(self, length, roughness, height_change, diameter=None, width=None, height=None, ):
        self.diameter = diameter
        self.width = width
        self.height = height
        self.length = length

        # Determine geometry from inputs
        if not diameter and not (height and width):
            raise Exception("Please specify geometry of cross section, "
                            "either a diameter of a circular pipe or height and width of a rectangular channel.")
        elif not diameter:  # Rectangular cross-section
            self.cross_sectional_area = self.width * self.height
            self.wetted_perimeter = self.width * 2 + self.height * 2
        else:  # Circular cross-section
            self.cross_sectional_area = circular_area(diameter)
            self.wetted_perimeter = circular_perimeter(diameter)

        self.roughness = roughness
        self.hydraulic_diameter = hydraulic_dia(perimeter=self.wetted_perimeter, area=self.cross_sectional_area)
        self.height_change = height_change
        self.velocity = None
        self.reynolds_number = None
        self.friction_factor = None
        self.dp_friction = None
        self.dp_height = None
        self.dp_minor = None
        self.dp_total = None

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
        self.dp_friction = dp_friction(friction_factor=self.friction_factor,
                                       fluid=fluid,
                                       pipe=self,
                                       velocity=self.velocity)

    def calc_dp_height(self, fluid):
        self.dp_height = fluid.density * self.height_change * ACCELERATION_GRAVITY

    def calc_dp_minor(self, *args):
        """Add K values together to find total minor losses"""

    def calc_dp_total(self, fluid):
        self.calc_dp_friction(fluid)
        self.calc_dp_height(fluid)
        self.dp_total = self.dp_height + self.dp_friction


def friction_factor_colebrook(pipe, reynolds_number, f_guess=0.04):
    """Returns the Darcy friction factor using the Colebrook-White equation"""

    if reynolds_number <= 2300:
        return 64 / reynolds_number

    elif reynolds_number > 2300:

        if 2300 < reynolds_number <= 4000:
            warnings.warn("Reynolds number is between 2300 and 4000 indicating transitional flow. "
                          "Darcy friction factor may be inaccurate.")

        f_guess = np.array(f_guess)
        roughness = pipe.roughness
        hydraulic_diameter = pipe.hydraulic_diameter

        a = 2.51 / reynolds_number
        b = roughness / 3.7 / hydraulic_diameter

        def colebrook(f):
            return -1 / np.sqrt(f) - 2 * np.log10(a * 1 / np.sqrt(f) + b)

        return fsolve(colebrook, f_guess)[0]


def reynolds(density, hydraulic_diameter, velocity, dynamic_viscosity):
    """Returns reynolds number of flow"""

    return density * hydraulic_diameter * velocity / dynamic_viscosity


def dp_friction(friction_factor, fluid, pipe, velocity):
    """Returns pressure drop due to frictional losses using Darcy-Weisbach"""

    length = pipe.length
    hydraulic_diameter = pipe.hydraulic_diameter
    density = fluid.density

    return length * friction_factor * density * velocity ** 2 / 2 / hydraulic_diameter


def hydraulic_dia(perimeter, area):
    """Returns hydraulic diameter given perimeter and area"""

    return 4 * area / perimeter


def circular_area(diameter):
    """Returns area of a circle given it's diameter"""

    return np.pi * diameter ** 2 / 4


def circular_perimeter(diameter):
    """Return the perimeter of a circle given the diameter"""

    return np.pi * diameter
