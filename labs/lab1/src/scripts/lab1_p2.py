# -*- coding: utf-8 -*-
#Solucion por Elkin

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel(name='lab1_p2')

# -----------------------------------------------

trabajadores = [1,2,3]
trabajos = [1,2,3,4,5]

tiempo_trabajadores = {1:8, 2:10, 3:6}
tiempo_trabajos = {1:4, 2:5, 3:3, 4:6, 5:2}
ganancia_trabajos = {1:50, 2:60, 3:40, 4:70, 5:30}


# Variable de decision
Model.x = Var(trabajadores, trabajos, domain=Binary) # Trabajadores

# Funcion objetivo:
Model.obj = Objective(expr = sum(ganancia_trabajos[j] * Model.x[i,j] for i in trabajadores for j in trabajos), sense=maximize)


# Restriccion de tiempo de los trabajadores
def restriccion_tiempo(model, i):
    return sum(tiempo_trabajos[j] * Model.x[i,j] for j in trabajos) <= tiempo_trabajadores[i]
        
Model.restr_tiempo = Constraint(trabajadores, rule = restriccion_tiempo)


# Restriccion de asignacion (cada trabajo se puede asignar una vez)
def restriccion_asignacion(model, j):
    return sum(model.x[i, j] for i in trabajadores) <= 1
Model.restriccion_asignacion = Constraint(trabajos, rule=restriccion_asignacion)


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()