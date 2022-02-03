"""
Script that converts CSV files to NPY files.
"""

import os
import numpy as np

CSV_DIRECTORY = "../../sample_data/csv/"
NPY_DIRECTORY = "../../sample_data/npy/"


# if not already done, convert sample csv files to npy format
'''
for i in range(16):
    filename = 'data_byte_' + str(i + 1).zfill(2)
    if not os.path.exists(INPUT_FOLDER_NPY + filename + '.npy'):
        # read csv file
        correlation_values = np.loadtxt(INPUT_FOLDER_CSV + filename + '.csv', delimiter=' ')
        print('Converting ' + filename + ' into npy...')
        # save to npy format
        np.save(INPUT_FOLDER_NPY + filename, correlation_values)
'''

# if not already done, convert real csv files to npy format
for i in range(16):
    filename = str(i)
    if not os.path.exists(NPY_DIRECTORY + filename + '.npy'):
        os.makedirs(NPY_DIRECTORY, exist_ok=True)
        print('Loading ' + filename + '.csv...')
        # "nan" values are replaced by 0
        correlation_values = np.genfromtxt(CSV_DIRECTORY + filename + '.csv', delimiter=' ', filling_values=0)

        print('Converting ' + filename + '.csv into npy...')
        np.save(NPY_DIRECTORY + str(i), correlation_values)



