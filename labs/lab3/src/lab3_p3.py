import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x, y = sp.symbols('x y')

funcion_rosenbrock = (x - 1)**2 + 100 * (y - x**2)**2

# Derivadas parciales
gradiente = [sp.diff(funcion_rosenbrock, var) for var in (x, y)]

# Hessiano (segunda derivada)
hessiano = sp.hessian(funcion_rosenbrock, (x, y))

# Expresiones simbólicas a funciones numéricas
funcion_numerica_rosenbrock = sp.lambdify((x, y), funcion_rosenbrock, 'numpy')
gradiente_numerico = sp.lambdify((x, y), gradiente, 'numpy')
hessiano_numerico = sp.lambdify((x, y), hessiano, 'numpy')

def newton_raphson_optimizacion(punto_inicial_a, punto_inicial_b, alph=1.0):
    trayectoria = [(punto_inicial_a, punto_inicial_b)]
    a_val, b_val = punto_inicial_a, punto_inicial_b
    while True:
        valor_gradiente = np.array(gradiente_numerico(a_val, b_val), dtype=float)
        if np.linalg.norm(valor_gradiente) < 0.001:
            break
        valor_hessiano = np.array(hessiano_numerico(a_val, b_val), dtype=float)
        paso = np.linalg.solve(valor_hessiano, valor_gradiente)
        a_val, b_val = np.array([a_val, b_val]) - alph * paso 
        trayectoria.append((a_val, b_val))
    return np.array(trayectoria)

a_inicial, b_inicial = 0, 10
alph = 1
trayectoria = newton_raphson_optimizacion(a_inicial, b_inicial, alph)

# Grafica
valores_a = np.linspace(-6, 6, 400)
valores_b = np.linspace(-10, 10, 400)
A, B = np.meshgrid(valores_a, valores_b)
Z = funcion_numerica_rosenbrock(A, B)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(A, B, Z, cmap='viridis', alpha=0.7)

trayectoria_a = trayectoria[:, 0]
trayectoria_b = trayectoria[:, 1]
trayectoria_z = funcion_numerica_rosenbrock(trayectoria_a, trayectoria_b)
ax.scatter(trayectoria_a, trayectoria_b, trayectoria_z, color='blue', label="Iteraciones", zorder=6)

optimo_a, optimo_b = trayectoria[-1]
optimo_z = funcion_numerica_rosenbrock(optimo_a, optimo_b)
ax.scatter([optimo_a], [optimo_b], [optimo_z], color='red', s=100, label="Óptimo", zorder=7)
ax.text(optimo_a, optimo_b, optimo_z, f'Óptimo: ({optimo_a:.2f}, {optimo_b:.2f}, {optimo_z:.2f})', color='black')

ax.set_xlim([-6, 6])
ax.set_ylim([-10, 10])
ax.set_zlim([0, 200000])

ax.set_title("Newton-Raphson en 3D - Iteraciones y Óptimo")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("f(x, y)")
ax.legend()

plt.show()
