import numpy as np
from PIL import Image

def getBit(data, bit_index):
    """Retrieve the bit at the specified index from the data."""
    byte_index = bit_index // 8
    bit_position = bit_index % 8
    return (data[byte_index] >> bit_position) & 1

def setBit(data, bit_index):
    """Set the bit at the specified index in the data."""
    byte_index = bit_index // 8
    bit_position = bit_index % 8
    data[byte_index] |= (1 << bit_position)

def create_custom_code(data, grid_size=256):
    """Create a custom encoded image from data."""
    grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
    bit_length = len(data) * 8
    bit_index = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if bit_index >= bit_length:
                return grid
            if getBit(data, bit_index):
                grid[i, j] = 255
            bit_index += 1
    return grid

def encode_to_image(data, grid_size=256, resolution = 1080):
    """Encode data into a binary grid and save as an image."""
    grid = create_custom_code(data, grid_size)
    img = Image.fromarray(np.stack([grid]*3, axis=-1), 'RGB')
    return np.array(img.resize((resolution, resolution), Image.Resampling.NEAREST))

def decode_from_image(img, grid_size=256):
    """Decode binary data from an image file."""
    img = Image.fromarray(img)
    img = img.convert('L')
    img = img.resize((grid_size, grid_size), Image.Resampling.BOX)

    grid = np.array(img)
    data = bytearray(grid_size * grid_size // 8)

    bit_index = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] > 128:
                setBit(data, bit_index)
            bit_index += 1

    return data

def example():
    # Example usage:
    test_string = "Hello, World!"
    data = test_string.encode()

    # Encode to image
    img = encode_to_image(data, grid_size=20)  # Use a smaller grid for visualization

    # Decode from image
    decoded_data = decode_from_image(img, grid_size=20)
    decoded_string = decoded_data.decode("utf-8", errors="ignore")

    # Display results
    img.show()
    print("Decoded String:", decoded_string)

if __name__ == "__main__":
    example()
