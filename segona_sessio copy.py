import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from Grid import Grid
from noise import pnoise2
#from perlin_noise import PerlinNoise

"""WIDTH, HEIGHT = map(int, input("Introdueix l'amplada i l'altura de la graella: ").split(' '))"""

def generate_humidity(height, width, rivers, seed):
    # Generar valors aleatoris de humitat entre 0 i 4 per a cada cel·la
    data = np.random.randint(0, 5, (height, width))
    data= (rivers+1)*data
    return data

def generate_vegetation(height, width, seed):
    # Generar valors aleatoris de vegetació entre 1 i 10 per a cada cel·la
    data = np.random.randint(0, 10, (height, width))
    return data

def generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed):
    terrain = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            terrain[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)
    terrain = terrain * -10  # Multiplica por -10 para invertir los valores (opcional)
    normalized_terrain = (terrain - np.min(terrain)) / (np.max(terrain) - np.min(terrain))  # Normaliza los valores entre 0 y 1
    discretized_terrain = np.floor(normalized_terrain * 10).astype(int)  # Discretiza los valores entre 0 y 9
    rivers = discretized_terrain<=1
    return rivers, discretized_terrain



"""def generate_rivers(height, width):
    noise = PerlinNoise()
"""


# Preguntar a l'usuari si vol generar nous fitxers
"""generate_new_files = input("Vols generar nous fitxers de dades per humitat i vegetació? (s/n): ")
if generate_new_files.lower() == 's':
    humidity = generate_humidity(HEIGHT, WIDTH)
    vegetation = generate_vegetation(HEIGHT, WIDTH)
    pd.DataFrame(humidity).to_csv("humidity.csv", index=False, header=False)
    pd.DataFrame(vegetation).to_csv("vegetation.csv", index=False, header=False)
else:
    humidity = pd.read_csv("humidity.csv", header=None).values
    vegetation = pd.read_csv("vegetation.csv", header=None).values"""



WIDTH,HEIGHT = 50,50

scale = 100.0  # Escala del ruido
octaves = 10  # Número de octavas para el ruido
persistence = 0.5  # Persistencia del ruido
lacunarity = 2.0  # Lacunaridad del ruido
seed = 42  # Semilla para generar el ruido




if True:
    rivers, terrain = generate_terrain(WIDTH, HEIGHT, scale, octaves, persistence, lacunarity, seed)
    humidity = generate_humidity(WIDTH,HEIGHT, rivers, seed)
    vegetation = generate_vegetation(WIDTH,HEIGHT, seed)

    pd.DataFrame(humidity).to_csv("humidity.csv", index=False, header=False)
    pd.DataFrame(vegetation).to_csv("vegetation.csv", index=False, header=False)
    pd.DataFrame(rivers).to_csv("rivers.csv", index=False, header=False)
    pd.DataFrame(terrain).to_csv("terrain.csv", index=False, header=False)
else:             
    humidity = pd.read_csv("humidity.csv", header=None).values
    vegetation = pd.read_csv("vegetation.csv", header=None).values
    rivers = pd.read_csv("rivers.csv", header=None).values
    terrain = pd.read_csv("terrain.csv", header=None).values
H = np.max(humidity)
V = np.max(vegetation)



# Generar la matriz de ríos







grid = Grid(HEIGHT, WIDTH, humidity, vegetation, rivers)
grid.init()
ani = grid.execute(n_iter=100)
ani = grid.ani
plt.show()
