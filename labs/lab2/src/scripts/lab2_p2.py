from pyomo.environ import *
import math
import numpy as np
import pandas as pd

Model = ConcreteModel()

numNodes=6

N=RangeSet(1, numNodes)

cost={(1,1):999, (1,2):1,   (1,3):1,   (1,4):2, (1,5):2,(1,6):1,\
      (2,1):1, (2,2):999,   (2,3):3,   (2,4):2, (2,5):3,(2,6):3,\
      (3,1):1, (3,2):3,   (3,3):999,   (3,4):3, (3,5):2,(3,6):3,\
      (4,1):2, (4,2):2,   (4,3):3,   (4,4):999, (4,5):1,(4,6):2,\
      (5,1):2, (5,2):3,   (5,3):3,   (5,4):1, (5,5):999,(5,6):3,\
      (6,1):1, (6,2):2,   (6,3):1,   (6,4):3, (6,5):3,(6,6):999}

# VARIABLES****************************************************************************
Model.x = Var(N,N, domain=Binary)
Model.u = Var(N, domain=NonNegativeReals)

Model.obj = Objective(expr = sum(cost[i,j]* Model.x[i,j] for i in N for j in N), sense=minimize)

def source_rule(Model,i):
    if i==1:
        return sum(Model.x[i,j] for j in N)==1
    else:
        return Constraint.Skip
Model.source=Constraint(N, rule=source_rule)

def destination_rule(Model,j):
    if j==1:
        return sum(Model.x[i,j] for i in N)==1
    else:
        return Constraint.Skip
Model.destination=Constraint(N, rule=destination_rule)

def MTZ_rule(Model, i, j):
    if i != j:
        return ((Model.u[i] - Model.u[j]) + (len(N)-1)*Model.x[i,j]) <= (len(N) - 2)
    else:
        return Constraint.Skip
Model.mtz=Constraint(N,N, rule=MTZ_rule)

def subtour_rule(Model):
    return Model.u[1] == 1
Model.stour=Constraint(rule=subtour_rule)

# APPLYING THE SOLVER******************************************************************
SolverFactory('glpk').solve(Model)

Model.display()