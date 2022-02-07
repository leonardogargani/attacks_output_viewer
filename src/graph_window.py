"""
Window containing the detailed plot of a single byte.
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic
import csv

import controller_window

MAIN_WINDOW_UI = 'ui/main_window.ui'
GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = "../sample_data/npy/"


class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.peak_line = None
        self.correlation_values = None
        uic.loadUi(GRAPH_WINDOW_UI, self)
        self.setWindowTitle('Detailed plot')
        self.lines = [None] * 256
        self.controller_window = controller_window.ControllerWindow(self)

        self.graph_widget.scene().sigMouseClicked.connect(self.graph_click)

    # overriding the closeEvent default function
    def closeEvent(self, event):
        self.controller_window.close()

    def graph_click(self, click):
        print('clicked on ' + str(click.pos().x()) + ' | ' + str(click.pos().y()))

    def generate_plot(self, byte_number):
        self.correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy', mmap_mode='r')
        print('Generating the plot...')

        # plot only data points that are currently visible (smooth when zoomed in)
        self.graph_widget.setClipToView(True)

        # Enable downsampling with:
        # - ds=0.1 (reduction factor for the visible samples)
        # - auto=True (automatically pick ds based on visible range)
        # - mode='subsample' (fastest but least accurate method)
        self.graph_widget.setDownsampling(ds=0.1, auto=True, mode='peak')

        with open('../sample_data/txt/peak.txt') as peaks_file:
            csv_reader = csv.reader(peaks_file)
            rows = list(csv_reader)
            self.peak_line = int(rows[byte_number][0])

        self.controller_window.create_scrollarea()
        self.controller_window.show()

    def add_curve(self, line_number):
        # plot a line with:
        # - skipFiniteCheck=True (because we know that no NaN values are in our data this help speed up plot time)
        # - clickable=True (make the curve clickable: when clicked, the signal sigClicked is emitted)
        self.lines[line_number] = self.graph_widget.plot(self.correlation_values[:, line_number],
                                                         pen=pg.intColor(line_number),
                                                         skipFiniteCheck=True,
                                                         clickable=True)

    def remove_curve(self, line_number):
        self.lines[line_number].clear()
        print('done')
        # force window activation to fix PyQt bug, which would require me to click
        # the graph window to gain the focus at OS system
        self.activateWindow()
