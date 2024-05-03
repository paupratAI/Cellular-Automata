import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from Grid import Grid
from perlin_noise import PerlinNoise

"""WIDTH, HEIGHT = map(int, input("Introdueix l'amplada i l'altura de la graella: ").split(' '))"""

def generate_humidity(height, width):
    # Generar valors aleatoris de humitat entre 0 i 4 per a cada cel·la
    data = np.random.randint(0, 5, (height, width))
    return data

def generate_vegetation(height, width):
    # Generar valors aleatoris de vegetació entre 1 i 10 per a cada cel·la
    data = np.random.randint(0, 10, (height, width))
    return data

def generate_rivers(height, width):
    noise = PerlinNoise()



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

if False:
    humidity = generate_humidity(100,100)
    vegetation = generate_vegetation(100,100)
    pd.DataFrame(humidity).to_csv("humidity.csv", index=False, header=False)
    pd.DataFrame(vegetation).to_csv("vegetation.csv", index=False, header=False)
else:             
    humidity = pd.read_csv("humidity.csv", header=None).values
    vegetation = pd.read_csv("vegetation.csv", header=None).values
H = np.max(humidity)
V = np.max(vegetation)

grid = Grid(HEIGHT, WIDTH, humidity, vegetation)
grid.init()
ani = grid.execute(n_iter=100)
ani = grid.ani
plt.show()


"""

greens = []

fire_status = np.zeros((HEIGHT, WIDTH))
fire_status[HEIGHT//2, WIDTH//2] = 1  # Iniciem el foc al centre

def update_colors(fire_status, humidity, vegetation):
    colors_cells = np.zeros((HEIGHT, WIDTH), dtype=int)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if humidity[i, j] > 0:
                if vegetation[i, j] > 0:
                    colors_cells[i, j] = humidity[i, j]
                else:
                    colors_cells[i,j] = H+1
            elif fire_status[i,j] >= 1:
                colors_cells[i,j] = H + 2 + vegetation[i,j]
            
    return colors_cells


def update_fire():
    new_status = fire_status.copy()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if fire_status[i, j] == 1 and humidity[i, j] > 0:
                # Reduir la humitat abans de començar a cremar la vegetació
                humidity[i, j] -= 1
            elif fire_status[i, j] == 1 and humidity[i, j] <= 0:
                # Reduir la vegetació un cop la humitat és zero
                vegetation[i, j] -= 1
                if vegetation[i, j] <= 0:
                    new_status[i, j] = 2  # Cremat
                # Propagar el foc
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < HEIGHT and 0 <= nj < WIDTH:
                        if fire_status[ni, nj] == 0:
                            new_status[ni, nj] = 1
    return new_status, humidity, vegetation





colors_cells = update_colors(fire_status, humidity, vegetation)
fig, ax = plt.subplots()

ll = [(0.15*(i/(H)) + 0.15, 0.5*(i/(H)) + 0.2, 0.05) for i in range(1,H+1)]

veg_fuego_ll = [(0.15*(i/(V)) + 0.7, 0.5*(i/(V)) + 0.2, 0.05) for i in range(1,V+1)]

ll.reverse()
colors = [(0.8, 0.9, 0)] + ll + [(1,1,0)] + [(0, 0, 0)] + veg_fuego_ll    # 0 humedad, 1->H humedad, no vegetation, fuego1(0->Veg_max), fuego2(quemado) 
#           0             1->H     H+1          H+2       H+3->H+3+V

print(len(colors))
print(np.max(colors))
#print(colors)
cmap = ListedColormap(colors)
norm = plt.Normalize(0, H+2+V)  # Normalitzar els valors per als tres estats i la vegetació
img = ax.imshow(colors_cells, cmap=cmap, norm=norm, interpolation='nearest')


def animate(t):

    global colors_cells
    global fire_status

    img.set_cmap(cmap)
    plt.draw()
    
    fire_status, humidity, vegetation = update_fire()
    colors_cells = update_colors(fire_status, humidity, vegetation)
    img.set_data(colors_cells)
    ax.set_title(f'Step {t}')

ani = FuncAnimation(fig, animate, frames=100, repeat=False)
plt.show()
"""