import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd

# Leemos el CSV
try:
    data = pd.read_csv('trajectory.csv')
except FileNotFoundError:
    print("Error: The file 'trajectory.csv' was not found.")
    exit()

# Extraemos los datos
x = data['x'].values
z = data['z'].values
vx = data['vx'].values
vz = data['vz'].values

# Creamos el plot 2D
fig, ax = plt.subplots(figsize=(10, 8), dpi=100)

# EJES
x_min, x_max = np.min(x), np.max(x)
z_min, z_max = np.min(z), np.max(z)
ax.set_xlim([x_min, x_max])
ax.set_ylim([z_min, z_max])
ax.set_xlabel('X (m)')
ax.set_ylabel('Z (m)')
ax.set_title('Movimiento de la partícula en el plano XZ')
ax.grid(True)

# Inicializamos linea y punto
line, = ax.plot([], [], label='Particle trajectory', color='b')
point, = ax.plot([], [], 'ro', label='Particle') #Partícula
quiver_v = None

# Factor de escala para los vectores
scale_factor_velocity = 0.0003

# Inicializamos función para la animación
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(i):
    if i >= len(x):
        return line, point
    
    # Actualizamos la linea de trayectoria
    line.set_data(x[:i+1], z[:i+1])
    
    # Actualizamos la posición del punto
    point.set_data([x[i]], [z[i]])
    
    # Borramos el quiver anterior
    global quiver_v
    if quiver_v is not None:
        quiver_v.remove()
    
    # Dibujamos el siguiente quiver para la velocidad
    quiver_v = ax.quiver(x[i], z[i], 
                         vx[i] * scale_factor_velocity, 
                         vz[i] * scale_factor_velocity, color='r')
    
    return line, point, quiver_v

ani = FuncAnimation(fig, animate, frames=len(x), init_func=init, interval=0.1, blit=False)

ani.save("particle_motion_XZ_plane.gif", writer=PillowWriter(fps=60))

plt.legend()
plt.show()
