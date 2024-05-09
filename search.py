from encode import create_video
from decode_video import decode
import os
import matplotlib.pyplot as plt
import numpy as np
import csv

def setup_csv():
    with open('./res/test_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Iteration', 'ReedEC', 'Grid Size', 'Success', 'Video Size (bytes)'])

def update_csv(iteration, reedEC, grid_size, success, video_size):
    with open('./res/test_results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([iteration, reedEC, grid_size, success, video_size])

def test_parameters(source_file, output_video, destination_folder, reedEC, grid_size):
    try:
        create_video(source_file, output_video, reedEC, grid_size)
        decode(output_video, destination_folder, reedEC, grid_size)
        video_size = os.path.getsize(output_video)
        return True, video_size
    except Exception as e:
        print(f"Error with reedEC={reedEC}, grid_size={grid_size}: {str(e)}")
        video_size = os.path.getsize(output_video)
        return False, video_size

def plot_results(results, reedEC_values, grid_size_values, iteration):
    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(len(reedEC_values)):
        for j in range(len(grid_size_values)):
            if results[i, j] is not None:
                color = 'green' if results[i, j][0] else 'red'
                ax.scatter(grid_size_values[j], reedEC_values[i], color=color, s=5)
    ax.set_xlabel('Grid Size')
    ax.set_ylabel('Reed EC')
    ax.set_title(f'Parameter Test Results Iteration {iteration:05} (Green: Successful, Red: Failed)')
    ax.grid(True)
    plt.savefig(f'./res/parameter_test_results_iteration_{iteration:05}.png')
    plt.close(fig)

# Set up CSV file before starting tests
setup_csv()

# Parameters
source_file = './test/test100k.txt'
output_video = './test_video.mp4'
destination_folder = './decoded/'
reedEC_range = (1, 41)
grid_size_range = (50, 401)

# Generate orders
reedEC_values = np.arange(reedEC_range[0], reedEC_range[1] + 1)
grid_size_values = np.arange(grid_size_range[0], grid_size_range[1] + 1)

# Generate all combinations of reedEC and grid_size
parameter_combinations = [(r, g) for r in reedEC_values for g in grid_size_values]
np.random.shuffle(parameter_combinations)  # Shuffle to randomize the order completely

# Initialize result storage
results = np.full((len(reedEC_values), len(grid_size_values)), fill_value=None, dtype=object)

# Test all combinations
for iteration, (reedEC, grid_size) in enumerate(parameter_combinations):
    reed_index = np.where(reedEC_values == reedEC)[0][0]
    grid_index = np.where(grid_size_values == grid_size)[0][0]
    success, video_size = test_parameters(source_file, output_video, destination_folder, reedEC, grid_size)
    results[reed_index, grid_index] = (success, video_size)
    update_csv(iteration, reedEC, grid_size, success, video_size)
    plot_results(results, reedEC_values, grid_size_values, iteration)
