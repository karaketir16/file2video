

# reedN = 255
# reedK = 245


reedN = 10
reedK = 5


reedEC = reedN - reedK

grid_size = 16

# Constants
chunk_size = (reedK * ((grid_size*grid_size) // (reedN * 8))) - (4 + reedEC)
frame_rate = 20.0
width = 1080
height = 1080

