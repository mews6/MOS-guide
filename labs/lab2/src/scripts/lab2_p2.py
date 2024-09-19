from pyomo.environ import *
import math
import numpy as np
import pandas as pd

model = ConcreteModel()

numNodes=5

N=RangeSet(1, numNodes)

cost={(1,1):999, (1,2):5,   (1,3):2,   (1,4):999, (1,5):999,\
      (2,1):999, (2,2):999, (2,3):999, (2,4):999, (2,5):8,\
      (3,1):999, (3,2):999, (3,3):999, (3,4):3,   (3,5):999,\
      (4,1):999, (4,2):999, (4,3):999, (4,4):999, (4,5):2,\
      (5,1):999, (5,2):999, (5,3):999, (5,4):999, (5,5):999}

# VARIABLES****************************************************************************
Model.x = Var(N,N, domain=Binary)

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
Model.source=Constraint(N, rule=destination_rule)

def MTZ_rule(Model, i, j):
    if i != j:
        pass
    else:
        return Constraint.Skip
    pass