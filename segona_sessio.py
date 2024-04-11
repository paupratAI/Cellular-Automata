import numpy as np
import matplotlib.pyplot as plt

def read_simulated_data(rows, cols, min_value, max_value):
    """Genera dades simulades per a la capa de combustible o humitat."""
    return np.random.randint(min_value, max_value+1, size=(rows, cols))

def initialize_state(fuel_data, moisture_data):
    """Inicialitza l'estat basant-se en les dades de combustible."""
    # L'estat inicial: 0 - sense foc, 1 - foc
    state = np.zeros_like(fuel_data)
    # Iniciar el foc en el centre si és possible
    center = (fuel_data.shape[0] // 2, fuel_data.shape[1] // 2)
    if fuel_data[center] > 0:  # Només inicia foc si hi ha combustible
        state[center] = 1
    return state

def update_state(state, fuel, moisture):
    """Actualitza l'estat de l'incendi basant-se en el combustible i la humitat."""
    new_state = np.copy(state)
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] == 1:  # Si la cel·la està en flames
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < state.shape[0] and 0 <= nj < state.shape[1]:
                            if fuel[ni, nj] > 0 and moisture[ni, nj] < 2 and np.random.rand() < 0.5:
                                new_state[ni, nj] = 1
                                fuel[ni, nj] -= 1  # Consumir combustible
    return new_state

def plot_state(state, title):
    """Visualitza l'estat actual de l'incendi."""
    plt.imshow(state, cmap='hot', interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    plt.show()

# Simulació
rows, cols, min_val, max_val = 10, 10, 0, 2
fuel_data = read_simulated_data(rows, cols, min_val, max_val)
moisture_data = read_simulated_data(rows, cols, min_val, max_val)
state = initialize_state(fuel_data, moisture_data)

generations = 10  # Nombre de generacions per simular
for i in range(generations):
    plot_state(state, f"Generation {i + 1}")
    state = update_state(state, fuel_data, moisture_data)
