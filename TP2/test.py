
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Define universes
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
fan_speed   = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# 2. Membership functions
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['warm'] = fuzz.trimf(temperature.universe, [10, 20, 30])
temperature['hot']  = fuzz.trimf(temperature.universe, [20, 40, 40])

fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])

# 3. Rules
rule1 = ctrl.Rule(temperature['cold'], fan_speed['slow'])
rule2 = ctrl.Rule(temperature['warm'], fan_speed['slow'])
rule3 = ctrl.Rule(temperature['hot'], fan_speed['fast'])

# 4. Control system
fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
fan_sim  = ctrl.ControlSystemSimulation(fan_ctrl)

# 5. Provide input
fan_sim.input['temperature'] = 35

# 6. Compute
fan_sim.compute()

# 7. Output
print("Fan speed = ", fan_sim.output['fan_speed'])
