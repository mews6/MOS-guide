#Imports
from __future__ import division

from pyomo.environ import *
from pyomo.opt import SolverFactory

## Desarrollo

### Definicion de Modelo
Model = ConcreteModel()

numProjects = 11

p = RangeSet(1,numProjects)
value = {1:5, 2:3, 3:13, 4:1, 5:21, 6:2, 7:2, 8:5, 9:8, 10: 13, 11: 21}

