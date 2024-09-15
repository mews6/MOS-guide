from pyomo.environ import *
import math
import numpy as np
import pandas as pd

model = ConcreteModel()

locations = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12']
sensors = ['S1', 'S2', 'S3']
# Locations
costs = {'L1':250,
        'L2':100,
        'L3':200,
        'L4':250,
        'L5':300,
        'L6':120,
        'L7':170,
        'L8':150,
        'L9':270,
        'L10':130,
        'L11':100,
        'L12':230 }

#Sensors
consumption = {'S1':7, 
               'S2':4, 
               'S3':8}

#Both

comm_costs = {
    
}