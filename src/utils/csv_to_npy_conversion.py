"""Script to convert .csv files to .npy

Script that converts .csv files to .npy as a preprocessing step, so that data is optimized
both from loading time and memory usage perspectives.
"""

import os
import numpy as np

CSV_DIRECTORY = "../../data/input/csv/"
NPY_DIRECTORY = "../../data/output/npy/"


os.makedirs(NPY_DIRECTORY, exist_ok=True)

try:
    # If not already done, convert real csv files to npy format
    for byte_number in range(16):
        filename = str(byte_number)
        # "NaN" values are replaced by 0
        correlation_values = np.genfromtxt(f'{CSV_DIRECTORY}{filename}.csv', delimiter=',', filling_values=0)
        # Save to npy format
        print(f'Converting {filename}.csv into npy...')
        np.save(f'{NPY_DIRECTORY}{filename.zfill(2)}', correlation_values)

    print('Done.')

except FileNotFoundError:
    print('[ERROR] No .csv file found. Place your .csv files in the data/input/csv/ directory before.')
    os.rmdir(NPY_DIRECTORY)
    exit()
