import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
import pyqtgraph.exporters

INPUT_FILE = '../sample_data/data_byte_00.csv'
OUTPUT_FILE = '../sample_data/test.hdf5'

app = QApplication(sys.argv)

correlation_values = np.loadtxt(INPUT_FILE, delimiter=',')
time_instants = np.arange(correlation_values.shape[0])

# plot and export only the first row of the CSV file
plt = pg.plot(time_instants, correlation_values[:, 0])

exporter = pg.exporters.HDF5Exporter(plt.plotItem)
exporter.export(OUTPUT_FILE)

sys.exit(app.exec())
