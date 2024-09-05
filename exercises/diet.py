from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

'''
# Definicion variables alimento

c = carne = 1
a = arroz = 2
l = leche = 3
p = pan = 4

Todos los valores numericos vienen del enunciado.
'''
Model = ConcreteModel(name='dieta')

'''
N = Productos.

1 = Carne
2 = Arroz
3 = Leche
4 = Pan
'''
N = RangeSet(1,4)

# Variable de decisión, ligada a N *****************************************************************************************************************************************

Model.c = Var(N, domain=NonNegativeReals) 

'''
M = Caracteristicas de los productos.

1 = Calorias
2 = Proteinas
3 = Azucar
4 = Grasas 
5 = Carbohidratos

'''
M = RangeSet(1,5)

'''
Precios, los valores de las llaves corresponden a aquellos en N 
'''
p =  {1:3000,2:1000,3:600,4:700} 

'''
Variable objetivo,
'''
Model.obj = Objective(expr = sum(Model.c[i]*p[i] for i in N), sense=minimize)


'''
Datos de las comidas, cada dato esta organizado de forma que pueda leerse en el orden 
v[i][j]. donde 'i' es un valor de N (es decir, un alimento) y donde 'j' es un valor de M
(es decir, una caracteristica)
'''
v = {
    1:{ 
        1:287,
        2:26,
        3:0,
        4:19.3,
        5:0
    },
    2:{
        1:204,
        2:4.2,
        3:0.01,
        4:0.5,
        5:44.1
    },
    3:{
        1:146,
        2:8,
        3:13,
        4:8,
        5:11
    },
    4:{
        1:245,
        2:6,
        3:25,
        4:0.8,
        5:55
    }
}

'''
Limites.

Ligados a M
'''
L = {
    1: 1500,
    2: 63,
    3: 25,
    4: 50,
    5: 200
}

def inferior(Model, j):
    if j != 1 and j != 2:
        return (sum(Model.c[i]*v[i][j] for i in N ) <= L[j]) 
    else:
        return Constraint.Skip    
Model.inferior = Constraint(M, rule=inferior)

def superior(Model, j):
    if j == 1 or j == 2:
        return (sum(Model.c[i]*v[i][j] for i in N) >= L[j])
    else:
        return Constraint.Skip
Model.superior = Constraint(M, rule=superior)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()