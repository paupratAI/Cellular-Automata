import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

# Constants
WIDTH, HEIGHT = 20, 20  # Dimensions de la graella

def generate_humidity(height, width):
    # Generar valors aleatoris de humitat entre 0 i 4 per a cada cel·la
    data = np.random.randint(0, 5, (height, width))
    return data

def generate_vegetation(height, width):
    # Generar valors aleatoris de vegetació entre 1 i 10 per a cada cel·la
    data = np.random.randint(1, 11, (height, width))
    return data

# Preguntar a l'usuari si vol generar nous fitxers
generate_new_files = input("Vols generar nous fitxers de dades per humitat i vegetació? (s/n): ")
if generate_new_files.lower() == 's':
    humidity = generate_humidity(HEIGHT, WIDTH)
    vegetation = generate_vegetation(HEIGHT, WIDTH)
    pd.DataFrame(humidity).to_csv("humidity.csv", index=False, header=False)
    pd.DataFrame(vegetation).to_csv("vegetation.csv", index=False, header=False)
else:
    humidity = pd.read_csv("humidity.csv", header=None).values
    vegetation = pd.read_csv("vegetation.csv", header=None).values

fire_status = np.zeros((HEIGHT, WIDTH))
fire_status[HEIGHT//2, WIDTH//2] = 1  # Iniciem el foc al centre

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
    return new_status

fig, ax = plt.subplots()
colors = ['yellow', 'orange', 'red']  
cmap = ListedColormap(colors)
norm = plt.Normalize(0, 2)  # Normalitzar els valors per als tres estats
img = ax.imshow(fire_status, cmap=cmap, norm=norm, interpolation='nearest')
ax.axis('off')

def animate(t):
    global fire_status
    fire_status = update_fire()
    img.set_data(fire_status)
    ax.set_title(f'Step {t}')

ani = FuncAnimation(fig, animate, frames=50, repeat=False)
plt.show()
