"""
Script that converts CSV files to NPY files.
"""

import os
import numpy as np

CSV_DIRECTORY = "../../data/input/csv/"
NPY_DIRECTORY = "../../data/output/npy/"


# if not already done, convert real csv files to npy format
for i in range(16):
    filename = str(i)
    if not os.path.exists(NPY_DIRECTORY + filename.zfill(2) + '.npy'):
        os.makedirs(NPY_DIRECTORY, exist_ok=True)
        print('Loading ' + filename + '.csv...')
        # "nan" values are replaced by 0
        correlation_values = np.genfromtxt(CSV_DIRECTORY + filename + '.csv', delimiter=' ', filling_values=0)
        print('Converting ' + filename + '.csv into npy...')
        # save to npy format
        np.save(NPY_DIRECTORY + str(i).zfill(2), correlation_values)

