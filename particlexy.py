import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd

# Leemos los datos de trayectoria desde el archivo CSV
try:
    data = pd.read_csv('trajectory.csv')
except FileNotFoundError:
    print("Error: El archivo 'trajectory.csv' no fue encontrado.")
    exit()

# Extraemos los datos
x = data['x'].values
y = data['y'].values
vx = data['vx'].values
vy = data['vy'].values

# Crear la figura y el objeto 2D
fig, ax = plt.subplots(figsize=(10, 8), dpi=100)

# Configurar los ejes para asegurar la vista completa del plano
x_min, x_max = np.min(x), np.max(x)
y_min, y_max = np.min(y), np.max(y)
ax.set_xlim([x_min, x_max])
ax.set_ylim([y_min, y_max])
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_title('Movimiento de la partícula en el plano XY')
ax.grid(True)

# Inicializamos línea y punto
line, = ax.plot([], [], label='Trayectoria de la partícula', color='b')
point, = ax.plot([], [], 'ro', label='Partícula')
quiver_v = None

# Factor de escala para los vectores de velocidad
scale_factor_velocity = 0.0003

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# Función de animación llamada para cada cuadro
def animate(i):
    if i >= len(x):
        return line, point
    
    # Actualizamos la línea de trayectoria
    line.set_data(x[:i+1], y[:i+1])
    
    # Actualizamos la posición del punto
    point.set_data([x[i]], [y[i]])
    
    # Eliminamos quiver anterior
    global quiver_v
    if quiver_v is not None:
        quiver_v.remove()
    
    # Dibujamos nuevo quiver para la velocidad
    quiver_v = ax.quiver(x[i], y[i], 
                         vx[i] * scale_factor_velocity, 
                         vy[i] * scale_factor_velocity, color='r')
    
    return line, point, quiver_v

# Ajustamos el intervalo para aumentar la velocidad de la animación
ani = FuncAnimation(fig, animate, frames=len(x), init_func=init, interval=0.1, blit=False)

# Guardamos la animación como un GIF con mayor DPI
ani.save("movimiento_particula_plano_XY.gif", writer=PillowWriter(fps=60))

plt.legend()
plt.show()
