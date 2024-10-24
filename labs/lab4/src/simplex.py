import numpy as np

def metodo_simplex(coef_objetivo, restricciones, limites):

    num_vars_decision = restricciones.shape[1]  # Número de variables de decisión
    num_restricciones = restricciones.shape[0]  # Número de restricciones

    restricciones = np.hstack([restricciones, np.eye(num_restricciones)])  # Añadir variables de holgura

    tabla = np.hstack([restricciones, limites.reshape(-1, 1)])  # Crear la tabla simplex
    
    coef_objetivo_extendido = np.hstack([coef_objetivo, np.zeros(num_restricciones + 1)])  # Extender c
    tabla = np.vstack([tabla, coef_objetivo_extendido])  # Agregar fila objetivo

    while True:
        columna_pivote = np.argmin(tabla[-1, :-1])  # Buscar la columna pivote
        if tabla[-1, columna_pivote] >= 0:  # Condición de parada
            break
        
        cocientes = tabla[:-1, -1] / tabla[:-1, columna_pivote]  # Cociente mínimo
        cocientes = np.where(cocientes > 0, cocientes, np.inf)
        fila_pivote = np.argmin(cocientes)  # Buscar la fila pivote

        elemento_pivote = tabla[fila_pivote, columna_pivote]
        tabla[fila_pivote, :] /= elemento_pivote  # Hacer 1 el elemento pivote

        for i in range(tabla.shape[0]):
            if i != fila_pivote:
                tabla[i, :] -= tabla[i, columna_pivote] * tabla[fila_pivote, :]  # Operaciones de fila

    solucion_optima = np.zeros(num_vars_decision)
    for i in range(num_vars_decision):
        columna = tabla[:-1, i]
        if np.count_nonzero(columna) == 1 and np.sum(columna) == 1:
            solucion_optima[i] = tabla[np.where(columna == 1)[0], -1]

    valor_optimo = tabla[-1, -1]

    return solucion_optima, valor_optimo

# Función objetivo (3x1 + 2x2)
coef_objetivo = np.array([-3, -2])  # Maximizar, por lo que coef_objetivo debe ser negativo.

# Restricciones
restricciones = np.array([
    [2, 1],  # 2x1 + x2 <= 100
    [1, 1],  # x1 + x2 <= 80
    [1, 0]   # x1 <= 40
])

limites = np.array([100, 80, 40])

resultado, z_optimo = metodo_simplex(coef_objetivo, restricciones, limites)

print(f"Solución óptima: x1 = {resultado[0]}, x2 = {resultado[1]}")
print(f"Valor óptimo de Z: {z_optimo}")
