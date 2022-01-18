"""


"""

import os
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic


MAIN_WINDOW_UI = 'ui/mainwindow_v2.ui'
GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = "../sample_data/npy/"


class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi(GRAPH_WINDOW_UI, self)
        self.setWindowTitle('Detailed plot')

    def generate_plot(self, byte_number):

        correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy')

        print('Generating the plot...')

        for num in range(correlation_values.shape[1]):

            # plot only data points that are currently visible (smooth when zoomed in)
            self.graph_widget.setClipToView(True)

            # Enable downsampling with:
            # - ds=0.1 (reduction factor for the visible samples)
            # - auto=True (automatically pick ds based on visible range)
            # - mode='subsample' (fastest but least accurate method)
            self.graph_widget.setDownsampling(ds=0.1, auto=True, mode='subsample')

            # disable auto range before plotting for faster plots
            self.graph_widget.disableAutoRange()

            # plot each line with:
            # - skipFiniteCheck=True (because we know that no NaN values are in our data this help speed up plot time)
            # - connect='all' (connecting all the lines helps speed up the plot time)
            # - clickable=True (make the curve clickable: when clicked, the signal sigClicked is emitted)
            line = self.graph_widget.plot(correlation_values[:, num], pen=pg.intColor(num), skipFiniteCheck=True,
                                          connect='all', clickable=True)

            # re-enable auto range
            self.graph_widget.autoRange()

        print('Done.')


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graph_window = None
        uic.loadUi(MAIN_WINDOW_UI, self)
        self.setWindowTitle('Byte selector')
        self.create_buttons()

    def create_buttons(self):
        filenames = [f for f in os.listdir(NPY_DIRECTORY) if f.endswith('.npy')]
        row_index = 0
        column_index = 0
        for filename in sorted(filenames):
            byte_num = int(os.path.splitext(filename)[0])

            button = QtWidgets.QPushButton('Byte ' + str(byte_num))
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            button.setToolTip('click to show the plot')
            # due to python's scoping rules and closures, we need to capture byte_num
            button.clicked.connect(lambda state, x=byte_num: self.plot_byte(x))

            self.gridLayout.addWidget(button, row_index, column_index)

            # place the buttons in rows of 4 elements
            if (column_index % 3 == 0) and (column_index != 0):
                row_index += 1
                column_index = 0
            else:
                column_index += 1

    def plot_byte(self, byte_number):
        self.graph_window = GraphWindow()
        self.graph_window.top_label.setText("Byte #" + str(byte_number).zfill(2))
        self.graph_window.show()

        self.graph_window.generate_plot(byte_number)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
