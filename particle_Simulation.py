import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Leemos los datos del archivo CSV
data = pd.read_csv('trajectory.csv')

# Creamos la figura y el eje 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Inicializamos la gráfica
line, = ax.plot([], [], [], lw=2)
quiver = ax.quiver(0, 0, 0, 0, 0, 0, length=0.1, normalize=True)
point, = ax.plot([], [], [], 'ro')  # Punto rojo para indicar la posición del electrón

# Configuramos las etiquetas de los ejes con unidades de medida
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Trayectoria de la partícula en un campo magnético')

# Establecemos los límites de los ejes
ax.set_xlim(min(data['x']), max(data['x']))
ax.set_ylim(min(data['y']), max(data['y']))
ax.set_zlim(min(data['z']), max(data['z']))

# Creamos un cuadro de texto para mostrar las componentes del campo magnético
bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white", alpha=0.8)
text_info = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, bbox=bbox_props)

# Función de inicialización
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    quiver.set_segments([])
    point.set_data([], [])
    point.set_3d_properties([])
    text_info.set_text("")
    return line, quiver, point, text_info

# Actualización de la animación
def update(num):
    line.set_data(data['x'][:num], data['y'][:num])
    line.set_3d_properties(data['z'][:num])
    
    # Actualizamos el punto rojo de la posición del electrón
    point.set_data([data['x'][num]], [data['y'][num]])  # Convertimos en secuencia de un elemento
    point.set_3d_properties([data['z'][num]])  # Convertimos en secuencia de un elemento
    
    # Actualizamos el vector del campo magnético
    Bx = data['Bx'][num]
    By = data['By'][num]
    Bz = data['Bz'][num]
    quiver.set_segments([[[data['x'][num], data['y'][num], data['z'][num]], 
                          [data['x'][num] + Bx, data['y'][num] + By, data['z'][num] + Bz]]])
    
    # Actualizamos el cuadro de texto con las componentes del campo magnético
    text_info.set_text(
        f"Bx: {Bx:.2e} T, By: {By:.2e} T, Bz: {Bz:.2e} T"
    )
    return line, quiver, point, text_info
ani = FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, interval=5) # Creamos la animación

# Mostramos la animación
plt.show()



