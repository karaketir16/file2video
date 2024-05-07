import numpy as np
from PIL import Image

def string_to_binary(data):
    """Convert a string into a binary sequence."""
    return ''.join(f"{ord(c):08b}" for c in data)

def binary_to_string(binary_data):
    """Convert binary data back to a string, assuming 8-bit chunks representing characters,
    and excluding null characters."""
    characters = []
    for i in range(0, len(binary_data), 8):
        char_code = int(binary_data[i:i+8], 2)
        if char_code == 0:  # Skip null characters
            continue
        characters.append(chr(char_code))
    return ''.join(characters)

def create_custom_code(data, grid_size=20):
    """Create a custom encoded image from data."""
    binary_data = string_to_binary(data)
    total_cells = grid_size * grid_size
    padded_data = binary_data.ljust(total_cells, '0')

    grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            grid[i, j] = 255 if index < len(padded_data) and padded_data[index] == '1' else 0

    return grid

def encode_to_image(data, filename='encoded_image.png', grid_size=20):
    """Encode data into a binary grid and save as an image."""
    grid = create_custom_code(data, grid_size)
    img = Image.fromarray(grid, 'L')
    img = img.resize((1024, 1024), Image.Resampling.NEAREST)
    img.save(filename, 'PNG')  # Change to JPEG and adjust quality for testing JPEG compression
    return filename

def decode_from_image(filename, grid_size=20):
    """Decode binary data from an image file."""
    img = Image.open(filename).convert('L')
    img = img.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    grid = np.array(img)
    binary_data = ''.join('1' if pixel > 128 else '0' for row in grid for pixel in row)
    return binary_to_string(binary_data)


def compress_and_test(data, grid_size=20, low=0, high=100):
    """Binary search to find the minimum JPEG compression quality that allows correct decoding."""
    original_img = Image.fromarray(create_custom_code(data, grid_size), 'L')
    original_img = original_img.resize((1024, 1024), Image.Resampling.NEAREST)

    def test_compression(quality):
        filename = f'test_compression_{quality}.jpeg'
        original_img.save(filename, 'JPEG', quality=quality)
        decoded_data = decode_from_image(filename, grid_size)
        print("Actual Data: ", data)
        print("Decoded Data: ", decoded_data)
        print("Same: ", data == decoded_data)
        return data == decoded_data

    min_quality = high  # Start with the highest quality
    while low <= high:
        mid = (low + high) // 2
        if test_compression(mid):
            min_quality = mid  # Found a working quality level
            high = mid - 1     # Try to find a lower quality that still works
        else:
            low = mid + 1      # Increase quality because the current mid fails

    return min_quality

# Example usage
data = "hello world"
filename = encode_to_image(data, 'encoded_image.png')
decoded_data = decode_from_image(filename)
max_quality = compress_and_test(data)

print(f"Decoded data: {decoded_data}")
print(f"Max JPEG quality for accurate decoding: {max_quality}")
