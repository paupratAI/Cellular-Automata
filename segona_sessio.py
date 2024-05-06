import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from Grid import Grid
from noise import pnoise2

# Paràmetres
WIDTH, HEIGHT = 100, 100
n_iterations = 200
fire_init = [(0, 0), (0, 50), (50, 50)]
generate_new_grid = True

# Paràmetres de generació de terren
scale = 100.0  
octaves = 10
persistence = 0.5  
lacunarity = 2.0  
seed = 42  
threshold_water = 3



# Funcions de generació de dades
def generate_humidity(height, width, rivers, seed):
    data = np.random.randint(0, 8, (height, width))
    data= (rivers+1)*data
    return data

def generate_vegetation(height, width, seed):
    data = np.random.randint(0, 15, (height, width))
    return data

def generate_terrain(width, height, scale, octaves, persistence, lacunarity, seed, threshold_water):
    terrain = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            terrain[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)
    terrain = terrain * -10
    normalized_terrain = (terrain - np.min(terrain)) / (np.max(terrain) - np.min(terrain))
    discretized_terrain = np.floor(normalized_terrain * 10).astype(int)
    rivers = discretized_terrain<=threshold_water
    return rivers, discretized_terrain

# Generació de dades i emmagatzematge en arxius CSV
if generate_new_grid:
    rivers, _ = generate_terrain(WIDTH, HEIGHT, scale, octaves, persistence, lacunarity, seed, threshold_water)
    humidity = generate_humidity(WIDTH, HEIGHT, rivers, seed)
    vegetation = generate_vegetation(WIDTH, HEIGHT, seed)

    pd.DataFrame(humidity).to_csv("humidity.csv", index=False, header=False)
    pd.DataFrame(vegetation).to_csv("vegetation.csv", index=False, header=False)
    pd.DataFrame(rivers).to_csv("rivers.csv", index=False, header=False)
else:             
    humidity = pd.read_csv("humidity.csv", header=None).values
    vegetation = pd.read_csv("vegetation.csv", header=None).values
    rivers = pd.read_csv("rivers.csv", header=None).values

# Màxims valors d'humitat i vegetació
H = np.max(humidity)
V = np.max(vegetation)

# Creació i execució de la simulació
grid = Grid(HEIGHT, WIDTH, humidity, vegetation, rivers)
ani = grid.execute(n_iter=n_iterations, fire_init=fire_init)
ani = grid.ani
plt.show()
