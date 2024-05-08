
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
