import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pylab
import matplotlib.pyplot as plt

temperature = ctrl.Antecedent(np.arange(-20, 20,1), 'temperature')#quality to jest temp
forecast = ctrl.Antecedent(np.arange(0, 11,1), 'forecast')
conFan = ctrl.Consequent(np.arange(0, 26, 1), 'conFan')
#names
names = ['Freezing', 'Cool', 'Warm', 'Hot']
names1 = ['Claudy', 'Sunny']

temperature.automf(names=names)
forecast.automf(names=names1)

conFan['slow'] = fuzz.trimf(conFan.universe, [0, 0, 13])
conFan['medium'] = fuzz.trimf(conFan.universe, [0, 13, 25])
conFan['fast'] = fuzz.trimf(conFan.universe, [13, 25, 25])

temperature['Cool'].view()
#Rule1
rule1 = ctrl.Rule(temperature['Hot'] & forecast['Sunny'], conFan['fast'])
#rule1.view
rule1.view()
#Rule2
rule2 = ctrl.Rule(temperature['Freezing'] & forecast['Claudy'], conFan['slow'])
#Rule3
rule3 = ctrl.Rule(temperature['Warm'] & forecast['Claudy'], conFan['medium'])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['temperature'] = 19
tipping.input['forecast'] = 9

tipping.compute()

print(tipping.output['conFan'])


conFan.view(sim=tipping)
plt.show()