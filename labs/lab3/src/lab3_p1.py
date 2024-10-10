# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 08:52:40 2024

@author: mews6 (Jaime Torres)
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Definir la variable simbólica
x = sp.symbols('x')

#fuentes
f = x**5 - 8*x**3 + 10*x + 6
f_sharp = sp.diff(f, x)
f_double_sharp = sp.diff(f_sharp, x)  
f_num = sp.lambdify(x, f, 'numpy')
f_prime_num = sp.lambdify(x, f_sharp, 'numpy')
f_double_prime_num = sp.lambdify(x, f_double_sharp, 'numpy')

# Implementar el método de Newton-Raphson para encontrar los puntos críticos
def newton_raphson(x0, alpha=1, tol=0.001, max_iter=100):
    for _ in range(max_iter):
        f_prime_val = f_prime_num(x0)
        f_double_prime_val = f_double_prime_num(x0)
        
        # Calcular el nuevo valor de x usando el método de Newton-Raphson
        x1 = x0 - alpha * (f_prime_val / f_double_prime_val)
        
        # Verificar la convergencia
        if abs(f_prime_val) < tol:
            return x1
        
        x0 = x1
    return x0

f_num = sp.lambdify(x, f, 'numpy')
# Evaluar los puntos críticos para encontrar el mínimo y máximo global
x_vals = np.linspace(-6, 6, 400)
y_vals = f_num(x_vals)


# Función para encontrar todos los puntos críticos
def encontrar_puntos_criticos(x0_vals, alpha=1):
    puntos_criticos = []
    for x0 in x0_vals:
        x_critico = newton_raphson(x0, alpha)
        if x_critico not in puntos_criticos:
            puntos_criticos.append(x_critico)
    return puntos_criticos

# Encontrar los puntos críticos en el intervalo [-3, 3]
x0_vals = np.linspace(-3, 3, 10)
puntos_criticos = encontrar_puntos_criticos(x0_vals)

# Evaluar si son mínimos o máximos locales
minimos = []
maximos = []
for punto in puntos_criticos:
    segunda_derivada = f_double_prime_num(punto)
    if segunda_derivada > 0:
        minimos.append(round(punto, 4))
    elif segunda_derivada < 0:
        maximos.append(round(punto, 4))

# Evaluar los puntos críticos para encontrar el mínimo y máximo global
x_vals = np.linspace(-3, 3, 400)
y_vals = f_num(x_vals)

min_global = min(puntos_criticos, key=lambda x: f_num(x))
max_global = max(puntos_criticos, key=lambda x: f_num(x))

# Graficar la función
plt.figure(figsize=(8,6))
plt.plot(x_vals, y_vals, label='y = x^5 - 8x^3 + 10x + 6')


# Graficar los mínimos locales
for minimo in set(minimos):

    plt.plot(minimo, f_num(minimo), 'ko', label=f'Mínimo local en x={minimo:.3f}')

# Graficar los máximos locales
for maximo in set(maximos):

    plt.plot(maximo, f_num(maximo), 'ko', label=f'Máximo local en x={maximo:.3f}')

# Graficar el mínimo y máximo global
plt.plot(min_global, f_num(min_global), 'ro', label=f'Mínimo global en x={min_global:.3f}')
plt.plot(max_global, f_num(max_global), 'ro', label=f'Máximo global en x={max_global:.3f}')

# Configurar la gráfica
plt.title('Método de Newton-Raphson: Mínimos y Máximos Locales')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(True)
plt.legend()
plt.show()

