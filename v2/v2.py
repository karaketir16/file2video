import numpy as np
from PIL import Image

def string_to_binary(data):
    """Convert a string into a binary sequence."""
    return ''.join(f"{ord(c):08b}" for c in data)

def binary_to_string(binary_data):
    """Convert binary data back to a string, assuming 8-bit chunks representing characters."""
    characters = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return ''.join(characters)

def encode_to_image(data, filename='encoded_image.png', grid_size=20):
    """Encode data into a binary grid and save as an image."""
    binary_data = string_to_binary(data)
    total_cells = grid_size * grid_size
    padded_data = binary_data.ljust(total_cells, '0')

    grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            grid[i, j] = 255 if index < len(padded_data) and padded_data[index] == '1' else 0

    img = Image.fromarray(grid, mode='L')
    img = img.resize((1024, 1024), Image.Resampling.NEAREST)
    img.save(filename)
    return filename

def decode_from_image(filename, grid_size=20):
    """Decode binary data from an image file."""
    img = Image.open(filename).convert('L')
    img = img.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    grid = np.array(img)
    binary_data = ''.join('1' if pixel > 128 else '0' for row in grid for pixel in row)
    return binary_to_string(binary_data)

# Process the data
data = "hello world"
filename = encode_to_image(data)
decoded_data = decode_from_image(filename)
print(decoded_data)
