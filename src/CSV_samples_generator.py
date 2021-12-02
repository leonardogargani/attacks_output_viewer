import csv
import numpy as np

"""
Simple script to generate CSV files whose values are random real numbers between -1.0 and 1.0.
"""

NUMBER_OF_FILES = 16
NUMBER_OF_ROWS = 10000
NUMBER_OF_COLUMNS = 256

OUTPUT_FOLDER = "../sample_data/"

for i in range(NUMBER_OF_FILES):
    filename = OUTPUT_FOLDER + "data_byte_" + str(i) + ".csv"

    csv_rows = 2 * np.random.random_sample(size=(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)) - 1

    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_rows)
