import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

def generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed):
    terrain = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            terrain[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)
    return terrain

def add_rivers(terrain, num_rivers, river_width):
    height, width = terrain.shape
    for _ in range(num_rivers):
        start_x = np.random.randint(width)
        start_y = np.random.randint(height)
        angle = np.random.uniform(0, 2*np.pi)
        for i in range(1000):
            nx = int(start_x + i * np.cos(angle))
            ny = int(start_y + i * np.sin(angle))
            if 0 <= nx < width and 0 <= ny < height:
                terrain[ny, nx] -= river_width
                angle += np.random.uniform(-np.pi/4, np.pi/4)
            else:
                break
    return terrain


def discretize_terrain(terrain, num_levels):
    terrain_min = np.min(terrain)
    terrain_max = np.max(terrain)
    bins = np.linspace(terrain_min, terrain_max, num_levels + 1)
    return np.digitize(terrain, bins)

def visualize_map(terrain):
    plt.figure(figsize=(8, 8))
    plt.imshow(terrain, cmap='terrain')
    plt.colorbar(label='Height')
    plt.title('Terrain Map with Sharp Features')
    plt.show()

# Parámetros de entrada
width = 512  # Ancho del mapa
height = 512  # Alto del mapa
scale = 100.0  # Escala del ruido
octaves = 10  # Número de octavas para el ruido
persistence = 0.5  # Persistencia del ruido
lacunarity = 2.0  # Lacunaridad del ruido
seed = np.random.randint(0, 100)  # Semilla para generar el ruido
num_rivers = 1 # Número de ríos a generar
river_width = 0.005  # Anchura de los ríos (más estrechos)
num_levels = 5 # Número de niveles para discretizar el terreno

# Generar el terreno
terrain = generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed)

discretized_terrain = discretize_terrain(terrain, num_levels)

# Agregar ríos
terrain_with_rivers = add_rivers(discretized_terrain, num_rivers, river_width)

# Visualizar el mapa
visualize_map(terrain_with_rivers)
