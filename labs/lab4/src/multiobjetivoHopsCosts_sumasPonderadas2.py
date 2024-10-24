#Plot Imports
import matplotlib.pyplot as plt

#Pyomo Imports (Modelo Matematico)
from pyomo.environ import *
from pyomo.opt import SolverFactory

##############################################################################
##################### FUNCIONES ################################
##############################################################################

#FUNCION ELIMINAR COMPONENTE
def delete_component(Model, comp_name):
    list_del = [vr for vr in vars(Model)
                if comp_name == vr
                or vr.startswith(comp_name + '_index')
                or vr.startswith(comp_name + '_domain')]

    list_del_str = ', '.join(list_del)
    print('Deleting model components ({}).'.format(list_del_str))

    for kk in list_del:
        Model.del_component(kk)


##############################################################################
##################### MODELO ################################
##############################################################################

#Configuracion Iteraciones (Epsilon)----------------------------------------------------
numIteraciones = 11
iteraciones = range(numIteraciones)
epsilon_values = []  # Valores de epsilon para f1

for i in iteraciones:
    valorIter1 = i / (numIteraciones - 1)
    epsilon_values.append(valorIter1 * 20)  # Suponemos que el valor máximo de f1 es 20

#Creacion Modelo--------------------------------------------------------------
Model = ConcreteModel()

#sets & parameters------------------------------------------------------------
numNodes = 5
Model.N = RangeSet(1, numNodes)

#hops-----------------------------------------------------------------------
Model.h = Param(Model.N, Model.N, mutable=True, initialize=999)

Model.h[1, 2] = 1
Model.h[1, 3] = 1
Model.h[2, 5] = 1
Model.h[3, 4] = 1
Model.h[4, 5] = 1

#costos-----------------------------------------------------------------------
Model.c = Param(Model.N, Model.N, mutable=True, initialize=999)

Model.c[1, 2] = 10
Model.c[1, 3] = 5
Model.c[2, 5] = 10
Model.c[3, 4] = 5
Model.c[4, 5] = 5

#origen y destino-----------------------------------------------------------------------
s = 1
d = 5

#variables--------------------------------------------------------------------
Model.x = Var(Model.N, Model.N, domain=Binary)

# Excluir bucles dentro del mismo nodo (x[i, i] no debería existir)
def remove_self_loops_rule(Model, i):
    return Model.x[i, i] == 0
Model.self_loops = Constraint(Model.N, rule=remove_self_loops_rule)

# # FUNCIONES OBJETIVO*************************************************************

#Funcion hops
Model.f1 = sum(Model.x[i, j] * Model.h[i, j] for i in Model.N for j in Model.N)

#Funcion de costos
Model.f2 = sum(Model.x[i, j] * Model.c[i, j] for i in Model.N for j in Model.N)

#Restriccion nodo origen
def source_rule(Model, i):
    if i == s:
        return sum(Model.x[i, j] for j in Model.N if j != i) == 1  # Evitar x[i, i]
    else:
        return Constraint.Skip

Model.source = Constraint(Model.N, rule=source_rule)

#Restriccion nodo destino
def destination_rule(Model, j):
    if j == d:
        return sum(Model.x[i, j] for i in Model.N if i != j) == 1  # Evitar x[i, i]
    else:
        return Constraint.Skip

Model.destination = Constraint(Model.N, rule=destination_rule)

#Restriccion nodo intermedio
def intermediate_rule(Model, i):
    if i != s and i != d:
        return sum(Model.x[i, j] for j in Model.N if j != i) - sum(Model.x[j, i] for j in Model.N if j != i) == 0
    else:
        return Constraint.Skip

Model.intermediate = Constraint(Model.N, rule=intermediate_rule)

# PROCESO ITERATIVO: Método Epsilon-Constraint
f1_vec = []
f2_vec = []

for epsilon in epsilon_values:
    # Restriccion epsilon para f1
    Model.epsilon_constraint = Constraint(expr=Model.f1 <= epsilon)

    # Funcion objetivo minimizando f2
    Model.O_z = Objective(expr=Model.f2, sense=minimize)

    # Resolver el modelo
    result = SolverFactory('glpk').solve(Model)

    # Verificar si se encontró una solución factible
    if result.solver.status != 'ok' or result.solver.termination_condition != 'optimal':
        print(f'No se encontró solución en la iteración con epsilon={epsilon}')
        continue

    # Almacenar los valores de f1 y f2
    valorF1 = value(Model.f1)
    valorF2 = value(Model.f2)
    f1_vec.append(valorF1)
    f2_vec.append(valorF2)

    # Eliminar componentes para la siguiente iteracion
    delete_component(Model, 'O_z')
    delete_component(Model, 'epsilon_constraint')

# Graficar el frente de Pareto
plt.plot(f1_vec, f2_vec, 'o-')
plt.title('Frente óptimo de Pareto (Epsilon-Constraint)')
plt.xlabel('F1 (Saltos)')
plt.ylabel('F2 (Costos)')
plt.grid(True)
plt.show()
