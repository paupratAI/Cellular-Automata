import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2


def generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed):
    terrain = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            terrain[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)
    terrain = terrain * -10  # Multiplica por -10 para invertir los valores (opcional)
    normalized_terrain = (terrain - np.min(terrain)) / (np.max(terrain) - np.min(terrain))  # Normaliza los valores entre 0 y 1
    discretized_terrain = np.floor(normalized_terrain * 10).astype(int)  # Discretiza los valores entre 0 y 9
    return discretized_terrain


def add_rivers(terrain, num_rivers, river_width, min_height):
    height, width = terrain.shape
    rivers = np.zeros((height, width))  # Matriz para almacenar la presencia de ríos
    for _ in range(num_rivers):
        start_x = np.random.randint(width)
        start_y = np.random.randint(height)
        angle = np.random.uniform(0, 2*np.pi)
        for i in range(1000):
            nx = int(start_x + i * np.cos(angle))
            ny = int(start_y + i * np.sin(angle))
            if 0 <= nx < width and 0 <= ny < height:
                # Verificar si el terreno en la posición del río es mayor que la altura mínima especificada
                if terrain[ny, nx] > min_height:
                    rivers[ny, nx] = terrain[ny, nx]
                angle += np.random.uniform(-np.pi/8, np.pi/8)  # Ajusta ligeramente el ángulo
            else:
                break
    return rivers

# Parámetros
width = 100  # Ancho del mapa
height = 100  # Alto del mapa

scale = 100.0  # Escala del ruido
octaves = 10  # Número de octavas para el ruido
persistence = 0.5  # Persistencia del ruido
lacunarity = 2.0  # Lacunaridad del ruido
seed = np.random.randint(0, 100)  # Semilla para generar el ruido
num_rivers = 1 # Número de ríos a generar
min_height = 3  # Altura mínima para inundar el terreno con ríos

# Generar el terreno
terrain = generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed)
print(terrain==0)
print()
print(terrain)
boolean_array = terrain<=1
# Generar los ríos basados en el terreno con una altura mínima especificada
# Visualizar el terreno y el array booleano
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(terrain, cmap='terrain', vmin=0, vmax=9)  # Utilizamos cmap 'terrain' y especificamos los valores mínimo y máximo
plt.colorbar(label='Height')
plt.title('Terrain Map')

plt.subplot(1, 2, 2)
plt.imshow(boolean_array, cmap='binary')
plt.title('Boolean Array')

plt.tight_layout()
plt.show()