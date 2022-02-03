"""
Window containing the detailed plot of a single byte.
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic


MAIN_WINDOW_UI = 'ui/mainwindow.ui'
GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = "../sample_data/npy/"


class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi(GRAPH_WINDOW_UI, self)
        self.setWindowTitle('Detailed plot')

    def generate_plot(self, byte_number):
        correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy', mmap_mode='r')

        print('Generating the plot...')

        # plot only data points that are currently visible (smooth when zoomed in)
        self.graph_widget.setClipToView(True)

        # Enable downsampling with:
        # - ds=0.1 (reduction factor for the visible samples)
        # - auto=True (automatically pick ds based on visible range)
        # - mode='subsample' (fastest but least accurate method)
        self.graph_widget.setDownsampling(ds=0.1, auto=True, mode='peak')

        for num in range(correlation_values.shape[1]):

            # disable auto range before plotting for faster plots
            self.graph_widget.disableAutoRange()

            # plot each line with:
            # - skipFiniteCheck=True (because we know that no NaN values are in our data this help speed up plot time)
            # - connect='all' (connecting all the lines helps speed up the plot time)
            # - clickable=True (make the curve clickable: when clicked, the signal sigClicked is emitted)
            self.graph_widget.plot(correlation_values[:, num], pen=pg.intColor(num), skipFiniteCheck=True, clickable=True)

            # re-enable auto range
            self.graph_widget.autoRange()

        print('Done.')
