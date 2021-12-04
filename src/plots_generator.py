"""
Script to visualize the content of the CSV files all at once.
The content of each file, representing values of a single byte, has its own plot.
"""

import pyqtgraph as pg
import numpy as np
import sys
from PySide6.QtWidgets import QApplication

PLOTS_ROWS = 4
PLOTS_COLUMNS = 4

app = QApplication(sys.argv)
widget = pg.GraphicsLayoutWidget()

for plot_row in range(PLOTS_ROWS):
    for plot_column in range(PLOTS_COLUMNS):

        file_number_string = str(PLOTS_ROWS * plot_row + plot_column).zfill(len(str(PLOTS_ROWS * PLOTS_COLUMNS)))
        correlation_values = np.loadtxt('../sample_data/data_byte_' + file_number_string + '.csv', delimiter=',')
        print('Loading data_byte_' + file_number_string + '.csv...')

        time_instants = range(correlation_values.shape[0])

        plot = widget.addPlot(row=plot_row, col=plot_column)
        plot.setTitle('Byte #' + file_number_string)
        plot.setWindowTitle('Attacks output viewer')

        for num in range(correlation_values.shape[1]):
            plot.plot(time_instants, correlation_values[:, num])

print('Rendering the widget...')
widget.show()

sys.exit(app.exec())
