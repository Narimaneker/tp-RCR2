
"""
Problem Definition :
- determine the rating of a house based on its size, price and location. 
"""

""" 
Fuzzy variables 
- input variables :
    - size :
        - small (z-shaped) : 50-100
        - medium (triangle) : 70-100-130
        - large (s-shaped) : 100-150
    - price :
        - cheap (z-shaped) : 0-3000
        - moderate (trapezoid) : 2000-5000-7000-10000
        - expensive (s-shaped): 8000-13000
    - location :
        - poor (z-shaped) : 0-2.5
        - average (triangle): 2-4.5-6
        - good (triangle) : 5-6.5-9
        - excellent (s-shaped) : 7-10
- output variable :
    - rating : 
        - very low (z-shaped) : 0-2
        - low (triangle) : 1-3-5
        - medium (trapezoid) : 4-5-6-7
        - high (triangle) : 6-8-9
        - very high (s-shaped) : 8-10
"""

from matplotlib import pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --------------------------------------------------------
# 1. DEFINE UNIVERSES
# --------------------------------------------------------

size_fuzzy_variable = ctrl.Antecedent(np.arange(50, 201, 10), 'size')
price_fuzzy_variable = ctrl.Antecedent(np.arange(0, 20001, 1000), 'price')
location_fuzzy_variable = ctrl.Antecedent(np.arange(0, 11, 1), 'location')

rating_fuzzy_variable = ctrl.Consequent(np.arange(0, 11, 1), 'rating')

# --------------------------------------------------------
# 2. MEMBERSHIP FUNCTIONS
# --------------------------------------------------------

# ---- SIZE ----
size_fuzzy_variable['small']  = fuzz.zmf(size_fuzzy_variable.universe, 50, 100)
size_fuzzy_variable['medium'] = fuzz.trimf(size_fuzzy_variable.universe, [70, 100, 130])
size_fuzzy_variable['large']  = fuzz.smf(size_fuzzy_variable.universe, 100, 150)

# ---- PRICE ----
price_fuzzy_variable['cheap']    = fuzz.zmf(price_fuzzy_variable.universe, 0, 3000)
price_fuzzy_variable['moderate'] = fuzz.trapmf(price_fuzzy_variable.universe, [2000, 5000, 7000, 10000])
price_fuzzy_variable['expensive'] = fuzz.smf(price_fuzzy_variable.universe, 8000, 13000)

# ---- LOCATION ----
location_fuzzy_variable['poor']     = fuzz.zmf(location_fuzzy_variable.universe, 0, 2.5)
location_fuzzy_variable['average'] = fuzz.trimf(location_fuzzy_variable.universe, [2, 4, 6])
location_fuzzy_variable['good']    = fuzz.trimf(location_fuzzy_variable.universe, [5, 6, 9])
location_fuzzy_variable['excellent'] = fuzz.smf(location_fuzzy_variable.universe, 7, 10)

# ---- RATING (OUTPUT) ----
rating_fuzzy_variable['very_low']  = fuzz.zmf(rating_fuzzy_variable.universe, 0, 2)
rating_fuzzy_variable['low']       = fuzz.trimf(rating_fuzzy_variable.universe, [1, 3, 5])
rating_fuzzy_variable['medium']    = fuzz.trapmf(rating_fuzzy_variable.universe, [4, 5, 6, 7])
rating_fuzzy_variable['high']      = fuzz.trimf(rating_fuzzy_variable.universe, [6, 8, 9])
rating_fuzzy_variable['very_high'] = fuzz.smf(rating_fuzzy_variable.universe, 8, 10)

# --------------------------------------------------------
# 3. RULES (example rules, you can modify)
# --------------------------------------------------------


size_values  = ['small', 'medium', 'large']
price_values = ['cheap', 'moderate', 'expensive']
location_values  = ['poor', 'average', 'good', 'excellent']


rules = []

# 1. Poor location and expensive price → very low rating
rules.append(ctrl.Rule(location_fuzzy_variable['poor'] & price_fuzzy_variable['expensive'], rating_fuzzy_variable['very_low']))

# 2. Poor location and moderate price → low rating
rules.append(ctrl.Rule(location_fuzzy_variable['poor'] & price_fuzzy_variable['moderate'], rating_fuzzy_variable['low']))

# 3. Poor location and cheap price → medium rating
rules.append(ctrl.Rule(location_fuzzy_variable['poor'] & price_fuzzy_variable['cheap'], rating_fuzzy_variable['medium']))

# 4. Average location and expensive price → low rating
rules.append(ctrl.Rule(location_fuzzy_variable['average'] & price_fuzzy_variable['expensive'], rating_fuzzy_variable['low']))

# 5. Average location and moderate price → medium rating
rules.append(ctrl.Rule(location_fuzzy_variable['average'] & price_fuzzy_variable['moderate'] & size_fuzzy_variable['small'], rating_fuzzy_variable['medium']))
rules.append(ctrl.Rule(location_fuzzy_variable['average'] & price_fuzzy_variable['moderate'] & size_fuzzy_variable['medium'], rating_fuzzy_variable['medium']))
rules.append(ctrl.Rule(location_fuzzy_variable['average'] & price_fuzzy_variable['moderate'] & size_fuzzy_variable['large'], rating_fuzzy_variable['high']))

# 6. Average location and cheap price → high rating
rules.append(ctrl.Rule(location_fuzzy_variable['average'] & price_fuzzy_variable['cheap'], rating_fuzzy_variable['high']))

# 7. Good location and expensive price → medium rating (size compensates)
rules.append(ctrl.Rule(location_fuzzy_variable['good'] & price_fuzzy_variable['expensive'] & size_fuzzy_variable['large'], rating_fuzzy_variable['high']))
rules.append(ctrl.Rule(location_fuzzy_variable['good'] & price_fuzzy_variable['expensive'] & size_fuzzy_variable['medium'], rating_fuzzy_variable['medium']))

# 8. Good location and moderate price → high rating
rules.append(ctrl.Rule(location_fuzzy_variable['good'] & price_fuzzy_variable['moderate'], rating_fuzzy_variable['high']))

# 9. Good location and cheap price → very high rating
rules.append(ctrl.Rule(location_fuzzy_variable['good'] & price_fuzzy_variable['cheap'], rating_fuzzy_variable['very_high']))

# 10. Excellent location and expensive price → high rating
rules.append(ctrl.Rule(location_fuzzy_variable['excellent'] & price_fuzzy_variable['expensive'], rating_fuzzy_variable['high']))

# 11. Excellent location and moderate price → very high rating
rules.append(ctrl.Rule(location_fuzzy_variable['excellent'] & price_fuzzy_variable['moderate'], rating_fuzzy_variable['very_high']))

# 12. Excellent location and cheap price → very high rating
rules.append(ctrl.Rule(location_fuzzy_variable['excellent'] & price_fuzzy_variable['cheap'], rating_fuzzy_variable['very_high']))



# --------------------------------------------------------
# 4. CONTROL SYSTEM
# --------------------------------------------------------

rating_ctrl = ctrl.ControlSystem(rules)

rating_sim = ctrl.ControlSystemSimulation(rating_ctrl)


def compute_output(input_size, input_price, input_location):
    rating_sim.input['size'] = input_size
    rating_sim.input['price'] = input_price
    rating_sim.input['location'] = input_location
    rating_sim.compute()
    return rating_sim.output['rating']

# --------------------------------------------------------
# 5. PROVIDE INPUTS
# --------------------------------------------------------

tests = [
    (80, 2500, 2),
    (120, 6000, 4),
    (160, 12000, 6),
    (90, 15000, 3),
    (140, 8000, 5),
    (200, 20000, 8),
    (70, 1000, 1),
    (110, 4000, 7),
    (170, 17000, 9),
]
for test in tests:
    input_size, input_price, input_location = test
    output_rating = compute_output(input_size, input_price, input_location)
    print(f"Input Size: {input_size}, Price: {input_price}, Location: {input_location} => Rating: {output_rating:.2f}")


# Optional: visualize

# variables = [size_fuzzy_variable, price_fuzzy_variable, location_fuzzy_variable, rating_fuzzy_variable]
# names = ["Size", "Price", "Location", "Rating"]
# for var, name in zip(variables, names):
#     var.view()                       # <-- draws on this window
#     plt.title(f"{name} Membership Functions")
#     plt.pause(0.001) 
# plt.show()            # <-- don't block, open all windows