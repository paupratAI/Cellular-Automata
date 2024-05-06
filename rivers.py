import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2


def generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed):
    """
    Genera un mapa de terreny usant el soroll Perlin.
    """
    terrain = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            terrain[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)
    terrain = terrain * -10  # Inverteix els valors perquè els volem al revés
    normalized_terrain = (terrain - np.min(terrain)) / (np.max(terrain) - np.min(terrain))  # Normalitza els valors entre 0 i 1
    discretized_terrain = np.floor(normalized_terrain * 10).astype(int)  # Discretitza els valors entre 0 i 9
    return discretized_terrain


def add_rivers(terrain, num_rivers, river_width, min_height):
    """
    Afegeix rius al mapa de terreny basant-se en una altura mínima.
    """
    height, width = terrain.shape
    rivers = np.zeros((height, width))  # Matriu per emmagatzemar la presència de rius
    for _ in range(num_rivers):
        start_x = np.random.randint(width)
        start_y = np.random.randint(height)
        angle = np.random.uniform(0, 2*np.pi)
        for i in range(1000):
            nx = int(start_x + i * np.cos(angle))
            ny = int(start_y + i * np.sin(angle))
            if 0 <= nx < width and 0 <= ny < height:
                # Verificar si el terreny en la posició del riu es major que l'alçada mínima especificada
                if terrain[ny, nx] > min_height:
                    rivers[ny, nx] = terrain[ny, nx]
                angle += np.random.uniform(-np.pi/8, np.pi/8)  
            else:
                break
    return rivers

# Paràmetres
width = 100  # Amplada del mapa
height = 100  # Alçada del mapa

scale = 100.0  # Escala del soroll
octaves = 10  # Octaves del soroll
persistence = 0.5  # Persistència del soroll
lacunarity = 2.0  # Lacunaritat del soroll
seed = np.random.randint(0, 100)  # Llavor del soroll
num_rivers = 1 # Número de rius
min_height = 3  # Alçada mínima del riu

# Generar el terreny
terrain = generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed)
print(terrain==0)
print()
print(terrain)
boolean_array = terrain<=1

# Visualitzar el terreny i la matriu boleana
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(terrain, cmap='terrain', vmin=0, vmax=9)  # Utilitza el mapa de colors 'terrain'
plt.colorbar(label='Height')
plt.title('Terrain Map')

plt.subplot(1, 2, 2)
plt.imshow(boolean_array, cmap='binary')
plt.title('Boolean Array')

plt.tight_layout()
plt.show()