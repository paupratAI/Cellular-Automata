import matplotlib.pyplot as plt

def apply_rule(rule, left, center, right):
    """
    Aplica la regla del autòmat cel·lular a un conjunt de tres cèl·lules.

    Args:
    rule (int): Número de la regla en decimal.
    left (int): Estat de la cèl·lula esquerra.
    center (int): Estat de la cèl·lula central.
    right (int): Estat de la cèl·lula dreta.

    Returns:
    int: Nou estat de la cèl·lula central basat en la regla.
    """
    binary_rule = f"{rule:08b}"
    index = 7 - (left*4 + center*2 + right*1)
    return int(binary_rule[index])

def generate_initial_state(length=100):
    """
    Genera un estat inicial per l'autòmat amb una sola cèl·lula activa al centre.

    Args:
    length (int): Longitud total de l'array de cèl·lules.

    Returns:
    list: Llista de cèl·lules amb una cèl·lula activa al centre.
    """
    return [0]*(length//2) + [1] + [0]*(length//2)

def evolve_multilayer(initial_cells, rules, generations=30):
    """
    Evoluciona un autòmat cel·lular multicapa a través de múltiples generacions.

    Args:
    initial_cells (list): Llista d'estats inicials de cèl·lules.
    rules (list of int): Llista de regles en decimal per a cada capa.
    generations (int): Nombre de generacions per evolucionar.

    Returns:
    list of list: Històric de totes les generacions evolucionades.
    """
    layers = [list(initial_cells) for _ in rules]
    history = [list(initial_cells)]
    
    for _ in range(generations):
        new_layers = []
        for layer_index, layer in enumerate(layers):
            rule = rules[layer_index]
            new_layer = [apply_rule(rule, layer[i-1] if i-1 >= 0 else 0, layer[i], layer[i+1] if i+1 < len(layer) else 0) for i in range(len(layer))]
            new_layers.append(new_layer)
        
        for i in range(len(layers[0])):
            sum_cells = sum(new_layers[layer][i] for layer in range(len(new_layers)))
            layers[0][i] = 1 if sum_cells > len(new_layers) / 2 else 0
        
        history.append(list(layers[0]))
    
    return history

def plot_evolution(history):
    """
    Visualitza la evolució del autòmat cel·lular usant matplotlib.

    Args:
    history (list of list): Històric de totes les generacions evolucionades.
    """
    plt.figure(figsize=(14, 8))
    plt.imshow(history, cmap='binary', interpolation='none')
    plt.title('Evolució de l\'Autòmat Cel·lular')
    plt.xlabel('Posició de la Cèl·lula')
    plt.ylabel('Generació')
    plt.show()

# Preguntar les regles a l'usuari
user_input = input("Introduïu les regles separades per comes (ex: 30,110,73): ")
rules = list(map(int, user_input.split(',')))

# Generar i evolucionar l'autòmat
cells = generate_initial_state()
history = evolve_multilayer(cells, rules, generations=30)  # Ajusteu el número de generacions com necessari
plot_evolution(history)
