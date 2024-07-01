import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd

try:
    data = pd.read_csv('trajectory.csv')
except FileNotFoundError:
    print("Error: The file 'trajectory.csv' was not found.")
    exit()

y = data['y'].values
z = data['z'].values
vy = data['vy'].values
vz = data['vz'].values

fig, ax = plt.subplots(figsize=(10, 8), dpi=100)

y_min, y_max = np.min(y), np.max(y)
z_min, z_max = np.min(z), np.max(z)
ax.set_xlim([y_min, y_max])
ax.set_ylim([z_min, z_max])
ax.set_xlabel('Y (m)')
ax.set_ylabel('Z (m)')
ax.set_title('Movimiento de la partícula en el plano YZ')
ax.grid(True)

line, = ax.plot([], [], label='Particle trajectory', color='b')
point, = ax.plot([], [], 'ro', label='Particle')
quiver_v = None

scale_factor_velocity = 0.0003

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(i):
    global quiver_v
    
    if i >= len(y):
        return line, point, quiver_v
    
    line.set_data(y[:i+1], z[:i+1])
    
    point.set_data([y[i]], [z[i]])
    
    if quiver_v is not None:
        quiver_v.remove()
    quiver_v = ax.quiver(y[i], z[i], 
                         vy[i] * scale_factor_velocity, 
                         vz[i] * scale_factor_velocity, color='r', label='Velocity' if i == 0 else "")
    
    return line, point, quiver_v

ani = FuncAnimation(fig, animate, frames=len(y), init_func=init, interval=0.1, blit=False)

ani.save("particle_motion_YZ_plane.gif", writer=PillowWriter(fps=60))

plt.legend()
plt.show()
