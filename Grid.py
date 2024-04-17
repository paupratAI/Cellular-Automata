import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap


class Grid:
    def __init__(self, height: int, width: int, humidity: np.array, vegetation: np.array) -> None:
        self.height = height
        self.width = width
        
        self.color_grid = np.array((0,0,0), (height, width))
        self.fire_status = np.zeros((height, width))
        self.vegetation = vegetation
        self.humidity = humidity

        self.updated_celdas = np.array()   # Vector que indica si una casilla ha sido actualizada, para colorear solo estas

    def init(self):
        """Inicializamos la cuadrícula, con vegetación, humedad y fuego"""
        self.fire_status[self.height//2, self.width//2] = 1  # Iniciem el foc al centre
        self.updated_celdas = np.ones((self.height, self.width))


    def update_humidity(self): 
        """Actualizamos la humedad de cada casilla, en caso de tener fuego, ya que al no tener la consideraremos quemada"""
        self.updated = np.hstack((i, j))
        pass

    def update_fire(self):
        """Actualizamos el estado del fuego, guardamos en un vector fuego == 1 las casillas cuyo fuego es 1, y aquellas que hayan propagado el fuego, lo pasamos a 2 (quemado)"""
        
        pass

    def update_colors(self):
        """Actualizamos los colores de las casillas, en función de la humedad, la vegetación y el fuego"""
        pass

    def next_step(self):
        pass

    def plot(self):
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
