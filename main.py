import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pylab
import matplotlib.pyplot as plt

temperature = ctrl.Antecedent(np.arange(0, 31,1), 'temperature')#quality to jest temp
forecast = ctrl.Antecedent(np.arange(0, 13,1), 'forecast')
conFan = ctrl.Consequent(np.arange(0, 26, 1), 'conFan')
#names
names = ['Freezing', 'Cool', 'Warm', 'Hot']
names1 = ['Rainy','Claudy', 'Sunny']

temperature.automf(names=names)
forecast.automf(names=names1)

conFan['slow'] = fuzz.trimf(conFan.universe, [0, 0, 13])
conFan['medium'] = fuzz.trimf(conFan.universe, [0, 13, 25])
conFan['fast'] = fuzz.trimf(conFan.universe, [13, 25, 25])

temperature['Cool'].view()
forecast['Claudy'].view()
#Rule1
rule1 = ctrl.Rule(temperature['Hot'] & forecast['Sunny'], conFan['fast'])
#rule1.view
rule1.view()
#Rule2
rule2 = ctrl.Rule(temperature['Freezing'] & forecast['Rainy'], conFan['slow'])
#Rule3
rule3 = ctrl.Rule(temperature['Warm'] & forecast['Claudy'], conFan['medium'])
#Rule4
rule4 = ctrl.Rule(temperature['Cool'] & forecast['Claudy'], conFan['medium'])
#Rule5
rule5 = ctrl.Rule(temperature['Hot'] & forecast['Rainy'], conFan['fast'])
#Rule6
rule6 = ctrl.Rule(temperature['Hot'] & forecast['Claudy'], conFan['fast'])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['temperature'] = 5
tipping.input['forecast'] = 0

tipping.compute()
#wsp = ((tipping.output['conFan']+10)/(25+10))*(1-0)+0
#print(wsp)
print(tipping.output['conFan'])
output_scal = (((((tipping.output['conFan'])+10)/(31+10))*(26-0)+0))
print(output_scal)

error = ((abs(29-28.26)/29))*100
print("Blad wzgledy wynosi: " + str(error))
conFan.view(sim=tipping)
plt.show()