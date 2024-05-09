import os

file_size_mb = 1 * 1024 * 1024 * 16  
file_path_mb = './test16MB.txt'

# Generate random data and write to file
with open(file_path_mb, 'wb') as f:
    f.write(os.urandom(file_size_mb))

file_path_mb
