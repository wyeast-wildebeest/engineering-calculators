import flow
import pint

"""
Test script for calculators
"""

# Define fluid
fluid_1 = flow.Fluid(name="water", density=1000, dynamic_viscosity=8.9e-4, temperature=25)

# Define pipe segment
pipe_1 = flow.PipeCircular(diameter=0.0125, length=1, roughness=0)

# Define boundary conditions
inlet_flow_rate = 1.2 / 60000  # m/s
outlet_pressure = 0  # Pa

# Solve for pressure drop
pipe_1.calc_velocity(inlet_flow_rate)
pipe_1.calc_reynolds(fluid_1)
pipe_1.calc_dp_friction(fluid_1)

# Output
print(pipe_1.dp)
print(pipe_1.reynolds_number)
