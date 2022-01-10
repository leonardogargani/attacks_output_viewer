"""Main window of the program

This file starts the program and shows one plot at a time.
The byte to be shown can be selected through a dropdown menu.
"""

import os
import sys

from PyQt5 import QtWidgets, uic
import numpy as np
import pyqtgraph as pg


UI_FILE = 'ui/mainwindow.ui'
INPUT_FOLDER = "../sample_data/"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(UI_FILE, self)
        self.populate_menubar()
        # plot the first byte by default
        self.plot_byte(0)

    def populate_menubar(self):
        filenames = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv')]
        for filename in sorted(filenames):
            action = QtWidgets.QAction(filename, self)
            byte_num = int(filename.partition('.')[0][-2:])
            # due to python's scoping rules and closures, we need to capture byte_num
            action.triggered.connect(lambda state, x=byte_num: self.plot_byte(x))
            self.menuSelect.addAction(action)

    def plot_byte(self, byte_number):
        filename = 'data_byte_' + str(byte_number).zfill(2) + '.csv'

        correlation_values = np.loadtxt(INPUT_FOLDER + filename, delimiter=',')
        print('Loading ' + filename + '...')

        time_instants = range(correlation_values.shape[0])

        for num in range(correlation_values.shape[1]):
            self.graph_widget.plot(time_instants, correlation_values[:, num], pen=pg.intColor(num))
            # Plot only data points that are currently visible
            # When plot is zoomed, less points are plotted and therefore it is smoother
            self.graph_widget.setClipToView(True)
            # Enable downsampling
            # ds = 0.1 is a dummy value because auto is set to True and therefore ds is automatically picked in function of visible range
            # mode='subsample', least accurate method but fast
            # see documentation for more details https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
            self.graph_widget.setDownsampling(ds=0.1, auto=True, mode='subsample')


        self.top_label.setText("Byte #" + str(byte_number).zfill(2))


def main():
    ## Switch to using white background and black foreground
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Rendering the window...')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
