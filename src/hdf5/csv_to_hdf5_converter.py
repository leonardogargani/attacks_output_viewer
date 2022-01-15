"""
Convert the 16 data_byte_xx.csv files to one single sample_data.hdf5 file.
This file contains 16 datasets and each dataset is a byte of the sample data.
"""

import numpy as np
import h5py

hdf5_filename = "sample_data.hdf5"

PLOTS_ROWS = 4
PLOTS_COLUMNS = 4

INPUT_FOLDER = "../../sample_data/"

# Create .hdf5 file in write mode
f = h5py.File(INPUT_FOLDER + hdf5_filename, 'w')

for plot_row in range(PLOTS_ROWS):
    for plot_column in range(PLOTS_COLUMNS):
        # Get the data from .csv file
        file_number = PLOTS_ROWS * plot_row + plot_column
        filename = 'data_byte_' + str(file_number).zfill(len(str(PLOTS_ROWS * PLOTS_COLUMNS))) + '.csv'
        correlation_values = np.loadtxt(INPUT_FOLDER + filename, delimiter=',')
        print('Loading ' + filename + '...')
        time_instants = range(correlation_values.shape[0])

        # The data is now stored in a numpy array, we can directly write that array to the dataset
        dset_name = 'data_byte_' + str(file_number).zfill(len(str(PLOTS_ROWS * PLOTS_COLUMNS)))
        f.create_dataset(dset_name, data=correlation_values)

