import matplotlib.pyplot as plt
import numpy as np


NPY_DIRECTORY = "../../sample_data/npy/"


byte_number = '1'
correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy', mmap_mode='r')

print('Exporting the plot as png...')

for num in range(correlation_values.shape[1]):
    plt.plot(correlation_values[:, num])

plt.savefig(str(byte_number).zfill(2) + '.png')

print('Done.')

