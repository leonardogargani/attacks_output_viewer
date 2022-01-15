"""
This script displays the content of the CSV files all at once.
The content of each file, representing values of a single byte, has its own plot.
"""

import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

PLOTS_ROWS = 4
PLOTS_COLUMNS = 4


INPUT_FOLDER = "../sample_data/"

app = QApplication(sys.argv)
widget = pg.GraphicsLayoutWidget()


for plot_row in range(PLOTS_ROWS):
    for plot_column in range(PLOTS_COLUMNS):

        file_number = PLOTS_ROWS * plot_row + plot_column
        filename = 'data_byte_' + str(file_number).zfill(len(str(PLOTS_ROWS * PLOTS_COLUMNS))) + '.csv'

        correlation_values = np.loadtxt(INPUT_FOLDER + filename, delimiter=',')
        print('Loading ' + filename + '...')

        time_instants = range(correlation_values.shape[0])

        plot = widget.addPlot(row=plot_row, col=plot_column)
        plot.setTitle('Byte #' + str(file_number))
        plot.setWindowTitle('Attacks output viewer')

        plot.setDownsampling(auto=True,mode='subsample')

        for num in range(correlation_values.shape[1]):
            plot.plot(time_instants, correlation_values[:, num])

print('Rendering the widget...')
widget.show()

sys.exit(app.exec())
