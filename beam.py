
class Beam:
    def __init__(self, length, elastic_modulus, moment_of_inertia):
        self.length = length
        self.elastic_modulus = elastic_modulus
        self.moment_of_inertia = moment_of_inertia

def cantilever_end_load(beam, load_F, x):
    reaction_1 = load_F
    shear = load_F
    moment_1 = load_F * beam.length
    moment_x = load_F * (x-beam.length)
    y = load_F * x**2 * (x - 3*beam.length) / 6 / beam.elastic_modulus / beam.moment_of_inertia
    y_max = load_F * beam.length**3 / 3 / beam.elastic_modulus / beam.moment_of_inertia

def cantilever_intermediate_load(beam, load_F, x, a):
    reaction_1 = load_F
    shear_ab = load_F
    moment_1 = load_F * a
    moment_ab = load_F * (x-a)
    moment_bc = 0
    y_ab = load_F * x**2 * (x - 3*a) / 6 / beam.elastic_modulus / beam.moment_of_inertia
    y_bc = load_F * a**2 * (a - 3*x) / 6 / beam.elastic_modulus / beam.moment_of_inertia
    y_max = load_F * a**2 * (a - 3*beam.length) / 6 / beam.elastic_modulus / beam.moment_of_inertia

def cantilever_uniform_load(beam, load_w, x):
    reaction_1 = load_w * beam.length
    moment_1 = load_w * beam.length**2 / 2
    shear = load_w * (beam.length-x)
    moment_x = -load_w * (beam.length-x)**2
    y = load_w * x**2 * (4*beam.length*x - x**2 - 6*beam.length**2) / 24 / beam.elastic_modulus / beam.moment_of_inertia
    y_max = -load_w * beam.length**4 / 8 / beam.elastic_modulus / beam.moment_of_inertia

def cantilever_moment_load(beam, load_M, x):
    reaction_1 = 0
    shear = 0
    moment_1 = load_M
    y = load_M * x**2 / 2 / beam.elastic_modulus / beam.moment_of_inertia
    y_max = load_M * beam.length**2 / 2 / beam.elastic_modulus / beam.moment_of_inertia

def simple_supports_center_load(beam, load_F, x):
    reaction_1 = load_F / 2
    reaction_2 = reaction_1
    shear_ab = reaction_1
    shear_bc = -reaction_2
    moment_ab = load_F * x / 2
    moment_bc = load_F * (beam.length-x) / 2
    y_ab = load_F * x * (4 * x**2 - 3 * beam.length**2) / 48 / beam.elastic_modulus / beam.moment_of_inertia
    y_max = -load_F * beam.length**3 / 48 / beam.elastic_modulus / beam.moment_of_inertia

def simple_supports_intermediate_load(beam, load_F, x, a):
    b = beam.length - a
    reaction_1 = load_F * b / beam.length
    reaction_2 = load_F * a / beam.length
    shear_ab = reaction_1
    shear_bc = -reaction_2
    moment_ab = load_F * b * x / beam.length
    moment_bc = load_F * a * (beam.length-x) / beam.length
    y_ab = (load_F * b * x * (x**2 + b**2 - beam.length**2)
            / 6 / beam.elastic_modulus / beam.moment_of_inertia / beam.length)
    y_bc = load_F * a * (beam.length-x) * (x**2 + a**2 - 2*beam.length*x)

def simple_supports_uniform_load(beam, load_w, x):
    reaction_1 = load_w * beam.length / 2
    reaction_2 = reaction_1
    shear = load_w * beam.length / 2 - load_w*x
    moment = load_w * x * (beam.length-x) / 2
    y = load_w * x * (2*beam.length * x**2 - x**3 - beam.length**3) / 24 / beam.elastic_modulus / beam.moment_of_inertia
    y_max = -5 * load_w * beam.length**4 / 384 / beam.elastic_modulus / beam.moment_of_inertia

def simple_supports_moment_load(beam, load_M, x, a):
    pass

def simple_supports_twin_load(beam, load_F, x, a):
    pass

def simple_supports_overhanging_load(beam, load_F, x, a):
    pass

