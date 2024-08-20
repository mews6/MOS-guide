# Zambia enfrenta una crisis humanitaria debido a desastres naturales, y es urgente transportar recursos esenciales a las áreas afectadas. SenecaLibre ha sido seleccionada para coordinar esta misión y debe utilizar su flota de aviones para transportar suministros críticos. Los recursos incluyen alimentos, medicinas, equipos médicos, agua potable y mantas, cada uno con su propio nivel de prioridad, peso y volumen. Cada avión tiene una capacidad máxima en términos de carga y espacio, y existen ciertas restricciones logísticas que deben respetarse.
# Datos del Problema:
# Recursos	Valor	Peso (TON)	Volumen (m^3)
# Alimentos Básicos	50	15	8
# Medicinas	100	5	2
# Equipos Médicos	120	20	10
# Agua Potable	60	18	12
# Mantas	40	10	6

# Avion	Capacidad (TON)	Capacidad volumetrica (m^3)
# Avión 1	30	25
# Avión 2	40	30
# Avión 3	50	35
# Restricciones de Almacenamiento de Recursos:
# Seguridad de Medicamentos	No se puede transportar a las Medicinas en el Avión 1 por la falta de condiciones para mantener la temperatura controlada, crucial para la efectividad de los medicamentos.
# Compatibilidad de Equipos Médicos y Agua Potable	Los Equipos Médicos y el Agua Potable no pueden ser transportados en el mismo avión debido al riesgo de contaminación cruzada. El derrame de agua podría dañar los equipos médicos delicados.

#Solucion por Elkin


from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel(name='lab1_p3')

# -----------------------------------------------

recursos = ['Alimentos', 'Medicinas', 'Equipos', 'Agua', 'Mantas']
aviones = ['Avion1', 'Avion2', 'Avion3']

valor = {'Alimentos':50, 'Medicinas':100, 'Equipos':120, 'Agua':60, 'Mantas':40}
peso = {'Alimentos':15, 'Medicinas':5, 'Equipos':20, 'Agua':18, 'Mantas':10}
volumen = {'Alimentos':8, 'Medicinas':2, 'Equipos':10, 'Agua':12, 'Mantas':6}

capacidad_peso = {'Avion1':30, 'Avion2':40, 'Avion3':50}
capacidad_volumen = {'Avion1':25, 'Avion2':30, 'Avion3':35}

# Variable de decision
Model.x = Var(recursos, aviones, domain=Binary) # Recursos

# Funcion objetivo:
Model.obj = Objective(expr = sum(valor[i] * Model.x[i,j] for i in recursos for j in aviones), sense=maximize)


# Restriccion de peso de los aviones
def restriccion_peso(model, j):
    return sum(peso[i] * Model.x[i,j] for i in recursos) <= capacidad_peso[j]

Model.restr_peso = Constraint(aviones, rule = restriccion_peso)


# Restriccion de volumen de los aviones
def restriccion_volumen(model, j):
    return sum(volumen[i] * Model.x[i,j] for i in recursos) <= capacidad_volumen[j]

Model.restr_volumen = Constraint(aviones, rule = restriccion_volumen)


# Restricciones de almacenamiento de recursos
def restriccion_almacenamiento(model):
    return Model.x['Medicinas','Avion1'] == 0
Model.restr_almacenamiento = Constraint(rule=restriccion_almacenamiento)

def restriccion_almacenamiento2(model):
    return Model.x['Equipos','Avion2'] + Model.x['Agua','Avion2'] <= 1
Model.restr_almacenamiento2 = Constraint(rule=restriccion_almacenamiento2)


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()