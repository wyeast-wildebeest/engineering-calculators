import flow
import pint

"""
Test script for calculators. 
All units must be SI (for now)
"""

# Define fluid
fluid_1 = flow.Fluid(name="water", density=1000, dynamic_viscosity=8.9e-4, temperature=25)

# Define pipe segment
pipe_1 = flow.Pipe(
    diameter=0.0125,
    # width=0.01,
    # height=0.0025,
    length=1,
    roughness=0,
    height_change=1
)

# Define boundary conditions
inlet_flow_rate = 1.4 / 60000  # m/s
outlet_pressure = 0  # Pa

# Solve for pressure drop
pipe_1.calc_velocity(inlet_flow_rate)
pipe_1.calc_reynolds(fluid_1)
pipe_1.calc_dp_total(fluid_1)

# Output
print(pipe_1.dp_friction)
print(pipe_1.dp_height)
print(pipe_1.dp_total)
print(pipe_1.reynolds_number)




