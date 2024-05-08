import numpy as np

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

def encode_to_image(data, grid_size=256, resolution=1080):
    """Encode data into a binary grid and resize to the specified resolution."""
    grid = create_custom_code(data, grid_size)
    # Resize the grid to exact resolution using interpolation
    scale_x = resolution / grid.shape[1]
    scale_y = resolution / grid.shape[0]
    resized_grid = np.zeros((resolution, resolution), dtype=np.uint8)

    for i in range(resolution):
        for j in range(resolution):
            x = int(i / scale_x)
            y = int(j / scale_y)
            resized_grid[i, j] = grid[x, y]

    return np.stack([resized_grid]*3, axis=-1)  # Create a 3-channel RGB image

def decode_from_image(img, grid_size=256):
    """Decode binary data from an image (as a numpy array)."""
    if len(img.shape) == 3:
        img = np.mean(img, axis=2).astype(np.uint8)
    # Resize image to grid size using simple downsampling
    scale = img.shape[0] // grid_size
    small_grid = img[::scale, ::scale]
    data = bytearray(grid_size * grid_size // 8)
    bit_index = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if small_grid[i, j] > 128:
                setBit(data, bit_index)
            bit_index += 1
    return data

def example():
    # Example usage:
    test_string = "Hello, World!"
    data = test_string.encode()

    # Encode to image
    img = encode_to_image(data, grid_size=20, resolution=1080)

    # Decode from image
    decoded_data = decode_from_image(img, grid_size=20)
    decoded_string = decoded_data.decode("utf-8", errors="ignore")

    # Print results
    print("Decoded String:", decoded_string)

if __name__ == "__main__":
    example()
