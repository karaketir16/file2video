from reedsolo import RSCodec
import random

# Initialize Reed-Solomon codec with ECC symbols
n = 128
k = 118
num_ec_symbols = n - k
rs = RSCodec(num_ec_symbols)

# Generate example data
data = bytes([i % 256 for i in range(4)])
print("Original Data:", data.hex(), len(data))

# Encode the data
encoded_data = rs.encode(data)
print("Encoded Data:", encoded_data.hex(), len(encoded_data))

# Introduce errors (e.g., corrupt up to num_ec_symbols//2 symbols)
import random
corrupted_data = bytearray(encoded_data)
error_positions = random.sample(range(len(corrupted_data)), (num_ec_symbols // 2))
for pos in error_positions:
    corrupted_data[pos] ^= 0xFF  # Flipping bits to introduce errors


# Decode the data without introducing errors
try:
    decoded_data, count, _= rs.decode(corrupted_data)  # Unpack the tuple
    is_correct = decoded_data == data
    print("Decoded Data:", decoded_data.hex())
except Exception as e:
    print("Decoding failed with exception:", str(e))
    is_correct = False

print("Data Correctly Decoded:", is_correct)
