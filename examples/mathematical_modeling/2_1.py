
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numProjects=8

p=RangeSet(1, numProjects)

value={1:2, 2:5, 3:4, 4:2, 5:6, 6:3, 7:1, 8:4}

# Decision Variable
Model.x = Var(p, domain=Binary)

# Objective Functions
Model.obj = Objective(expr = sum(Model.x[i]*value[i] for i in p), sense=maximize)

# Restrictions
Model.res1 = Constraint(expr = sum(Model.x[i] for i in p) == 2)

# Solver specifications
SolverFactory('glpk').solve(Model)

Model.display()