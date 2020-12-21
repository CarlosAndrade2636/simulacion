import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
data = int(input("ingrese un valor si le gusta la materia segun lo considere 0 nada, 5 mas o menos, 10 mucho:\n"))
data1 = int(input("ingrese un valor si le tiene algun conocimiento acerca de las materias en relacion a la carrera de Ingenieria civil segun lo considere: 0 nada, 5 mas o menos, 10 mucho:\n"))

gusto = ctrl.Antecedent(np.arange(0, 11, 1), 'gusto')
conocimiento = ctrl.Antecedent(np.arange(0, 11, 1), 'conocimiento')
afin = ctrl.Consequent(np.arange(0, 26, 1), 'afin')
gusto.automf(3)
conocimiento.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
afin['bajo'] = fuzz.trimf(afin.universe, [0, 0, 13])
afin['medio'] = fuzz.trimf(afin.universe, [0, 13, 25])
afin['alto'] = fuzz.trimf(afin.universe, [13, 25, 25])
gusto['average'].view()

rule1 = ctrl.Rule(gusto['poor'] | conocimiento['poor'], afin['bajo'])
rule2 = ctrl.Rule(conocimiento['average'], afin['medio'])
rule3 = ctrl.Rule(conocimiento['good'] | gusto['good'], afin['alto'])

afinping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
afinping = ctrl.ControlSystemSimulation(afinping_ctrl)


afinping.input['gusto'] = data
afinping.input['conocimiento'] = data1

afinping.compute()

print (afinping.output['afin'])
#afin.view(sim=afinping)
