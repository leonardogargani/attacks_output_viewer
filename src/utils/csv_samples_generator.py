"""
This script can be used to generate CSV files whose values are random real numbers between -1.0 and 1.0.
"""

import os
import csv
import numpy as np

NUMBER_OF_FILES = 16
NUMBER_OF_ROWS = 10000
NUMBER_OF_COLUMNS = 256

OUTPUT_FOLDER = "../../data/input/csv/"

for i in range(NUMBER_OF_FILES):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filename = OUTPUT_FOLDER + "data_byte_" + str(i+1).zfill(len(str(NUMBER_OF_FILES))) + ".csv"

    csv_rows = 2 * np.random.random_sample(size=(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)) - 1

    with open(filename, 'w') as csv_file:
        print('Generating ' + filename + '...')
        csv_writer = csv.writer(csv_file, delimiter=' ')
        csv_writer.writerows(csv_rows)

print('Done.')
