def apply_rule(rule, left, center, right):
    # Convert the rule number into a binary string
    binary_rule = f"{rule:08b}"
    
    # Index into the binary string based on the pattern of the cells
    index = 7 - (left*4 + center*2 + right*1)
    return int(binary_rule[index])

def generate_initial_state(length=30):
    # Generate an initial state with a single 1 in the center
    return [0]*(length//2) + [1] + [0]*(length//2)

def evolve(cells, rule, generations=15):
    for _ in range(generations):
        print(''.join(['█' if cell == 1 else ' ' for cell in cells]))  # Visualize the current generation
        # Apply the rule to each triplet of cells to create the next generation
        cells = [apply_rule(rule, cells[i-1], cells[i], cells[i+1] if i+1 < len(cells) else 0) for i in range(len(cells))]

# Example usage
rule = int(input("Enter the rule number: "))
cells = generate_initial_state()
evolve(cells, rule)
