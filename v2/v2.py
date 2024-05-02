import numpy as np
from PIL import Image

def string_to_binary(data):
    """Convert string to binary."""
    return ''.join(format(ord(i), '08b') for i in data)

def create_custom_code(data, grid_size=20):
    """Create a custom encoded image from data, using the entire grid to maximize capacity."""
    binary_data = string_to_binary(data)
    total_cells = grid_size * grid_size
    padded_data = binary_data.ljust(total_cells, '0')

    grid = np.zeros((grid_size, grid_size), dtype=np.uint8)  # black grid (reversing colors for clarity)
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            if index < len(padded_data) and padded_data[index] == '1':
                grid[i, j] = 255  # set white

    return grid

def binary_to_string(binary_data):
    """Convert binary data to string."""
    characters = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(b, 2)) for b in characters if '1' in b)

def decode_custom_code(binary_grid):
    """Decode custom encoded binary grid back to string."""
    grid_size = binary_grid.shape[0]
    binary_data = ''
    for i in range(grid_size):
        for j in range(grid_size):
            if binary_grid[i, j] == 255:  # white cells are 1s
                binary_data += '1'
            else:
                binary_data += '0'

    return binary_to_string(binary_data)

# Example data
data = "hello world"

# Encode to grid
grid = create_custom_code(data, 20)

# Convert grid to image and display for verification
image = Image.fromarray(grid)  # already in uint8
image = image.resize((400, 400), Image.Resampling.NEAREST)  # Scale up for visibility
image.show()

# Decode from grid
decoded_data = decode_custom_code(grid)
print(f"Decoded data: {decoded_data}")
