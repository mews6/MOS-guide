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
f_sharp = sp.diff(f, x)  # Primera derivada
f_double_sharp = sp.diff(f_sharp, x)  # Segunda derivada

def newton_raphson(x0, alpha=1, tol=0.001, max_iter=100):
    for _ in range(max_iter):
        f_prime_val = f_sharp(x0)
        f_double_prime_val = f_double_sharp(x0)
        
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


