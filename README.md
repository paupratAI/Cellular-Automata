# Wolfram Elementary Rules and Forest Fire Propagation Simulation

## Project Overview

This project consists of two sessions, each focusing on different implementations of cellular automata.

## Session 1: Wolfram's Elementary Rules

### Objectives
- Implement Wolfram's elementary rules for a cellular automaton in Python.
- Generalize to allow multiple rules in a multi-layer structure.
- Visualize the automaton's evolution using `matplotlib`.

### Key Functions
- **`apply_rule`**: Calculates the new state of a cell based on the rule.
- **`generate_initial_state`**: Creates the initial state with a single active central cell.
- **`evolve_multilayer`**: Evolves the automaton using multiple rules.
- **`plot_evolution`**: Visualizes the automaton's evolution over time.

### Conclusions
The code successfully simulates simple and multi-layer cellular automata, providing insight into how complex patterns emerge from basic rules.

## Session 2: Forest Fire Propagation

### Objectives
Simulate forest fire propagation using multi-layer cellular automata representing:
- Vegetation
- Humidity
- Water

### Key Layers and Rules
- **Fire Status**: Indicates if a cell is burning, burnt, or unburnt.
- **Humidity**: Decreases as a cell burns, affecting fire propagation.
- **Vegetation**: Decreases as a cell burns, stopping fire once depleted.
- **Water Bodies**: Generated using Perlin noise, blocks fire propagation.

### Python Implementation
- **`segona_sessio.py`**: Initializes data, then calls `Grid` to create the simulation.
- **`Grid.py`**: Contains the `Grid` class for simulating and animating the forest fire.

### Conclusions
The project defines interacting cellular automata rules to simulate forest fire propagation, demonstrating their potential for modeling complex phenomena. AI tools like ChatGPT and Copilot aided development, though manual adjustments were necessary for optimal results.
