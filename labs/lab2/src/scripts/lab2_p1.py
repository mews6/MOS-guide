from pyomo.environ import *
import math
import numpy as np


# Modelo
model = ConcreteModel()

# Conjuntos
origenes = ['Bogota', 'Medellin']
destinos = ['Cali', 'Barranquilla', 'Pasto', 'Tunja', 'Chia', 'Manizales']
costos = {
    ('Bogota', 'Cali'): 100, ('Medellin', 'Cali'): 2.5,
    ('Bogota', 'Barranquilla'): 2.5, ('Medellin', 'Barranquilla'): 100,
    ('Bogota', 'Pasto'): 1.6, ('Medellin', 'Pasto'): 2.0,
    ('Bogota', 'Tunja'): 1.4, ('Medellin', 'Tunja'): 1.0,
    ('Bogota', 'Chia'): 0.8, ('Medellin', 'Chia'): 1.0,
    ('Bogota', 'Manizales'): 1.4, ('Medellin', 'Manizales'): 0.8
}
demandas = {'Cali': 125, 'Barranquilla': 175, 'Pasto': 225, 'Tunja': 250, 'Chia': 225, 'Manizales': 200}
ofertas = {'Bogota': 550, 'Medellin': 700}

# Variables
model.x = Var(origenes, destinos, within=NonNegativeReals)

# Función objetivo: minimizar los costos de transporte
def objetivo(model):
    return sum(model.x[i, j] * costos[i, j] for i in origenes for j in destinos)
model.objetivo = Objective(rule=objetivo, sense=minimize)

# Restricción de oferta: no exceder la cantidad disponible en cada origen
def oferta_rule(model, i):
    return sum(model.x[i, j] for j in destinos) <= ofertas[i]
model.oferta = Constraint(origenes, rule=oferta_rule)

# Restricción de demanda: satisfacer la demanda en cada destino
def demanda_rule(model, j):
    return sum(model.x[i, j] for i in origenes) == demandas[j]
model.demanda = Constraint(destinos, rule=demanda_rule)

# Resolver el modelo
solver = SolverFactory('glpk')
solver.solve(model)

model.display()

# # Mostrar los resultados
# print("Toneladas transportadas:")
# for i in origenes:
#     for j in destinos:
#         print(f"{i} -> {j}: {model.x[i, j].value} tons")
