"""


"""

import os
import numpy as np

INPUT_FOLDER_CSV = "../sample_data/csv/"
INPUT_FOLDER_NPY = "../sample_data/npy/"


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
filename = '1'
if not os.path.exists(INPUT_FOLDER_NPY + filename.zfill(2) + '.npy'):
    os.makedirs(INPUT_FOLDER_NPY)
    print('Loading ' + filename + '.csv...')
    # "nan" values are replaced by 0
    correlation_values = np.genfromtxt(INPUT_FOLDER_CSV + filename + '.csv', delimiter=' ', filling_values=0)
    # save to npy format (16 times while waiting for the full data set)
    for i in range(16):
        print('Converting ' + filename + '.csv into npy...')
        np.save(INPUT_FOLDER_NPY + str(i + 1).zfill(2), correlation_values)

