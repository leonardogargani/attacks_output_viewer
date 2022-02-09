"""Detailed plot of a byte
Generate a detailed plot of a single byte. Show by default only the one line with the peak.
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic
import csv

import controller_window


MAIN_WINDOW_UI = 'ui/main_window.ui'
GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = "../data/output/npy/"


class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi(GRAPH_WINDOW_UI, self)
        self.peak_line = None
        self.peak_x = None
        self.peak_y = None
        self.correlation_values = None
        self.lines = [None] * 256
        self.controller_window = controller_window.ControllerWindow(self)

        #self.graph_widget.scene().sigMouseClicked.connect(self.graph_click)

    # Override the closeEvent function to close also the controller window
    def closeEvent(self, event):
        self.controller_window.close()

    def graph_click(self, click):
        print('clicked on ' + str(click.pos().x()) + ' | ' + str(click.pos().y()))

    def line_click(self, item, points):
        print("Line number " + item.name() + " clicked on x = {:.3f} y = {:.3f}".format(points.pos().x(), points.pos().y()))

    def generate_plot(self, byte_number):
        self.correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy', mmap_mode='r')
        print('Generating the plot...')

        # Plot only data points that are currently visible (smooth when zoomed in)
        self.graph_widget.setClipToView(True)

        # Enable downsampling with:
        # - ds=0.1 (reduction factor for the visible samples)
        # - auto=True (automatically pick ds based on visible range)
        # - mode='subsample' (fastest but least accurate method)
        self.graph_widget.setDownsampling(ds=0.1, auto=True, mode='peak')

        with open('../data/output/csv/peak.csv') as peaks_file:
            csv_reader = csv.reader(peaks_file)
            csv_rows = list(csv_reader)
            self.peak_line = int(csv_rows[byte_number][0])
            self.peak_x = int(csv_rows[byte_number][1])
            self.peak_y = float(csv_rows[byte_number][2])

        label_content = 'WARNING! This file contains only NaN values.' if self.peak_line == -1 \
            else 'The peak is in correspondence of curve ' + str(self.peak_line) + '.'

        self.graph_widget.addLine(x=self.peak_x)
        self.graph_widget.addLine(y=self.peak_y)

        self.controller_window.info_label.setText(label_content)
        self.controller_window.create_scrollarea()
        self.controller_window.show()

    def add_curve(self, line_number):
        # Plot a line with:
        # - skipFiniteCheck=True (because we know that no NaN values are in our data this help speed up plot time)
        # - clickable=True (make the curve clickable: when clicked, the signal sigClicked is emitted)
        self.lines[line_number] = self.graph_widget.plot(self.correlation_values[:, line_number],
                                                         pen=pg.intColor(line_number),
                                                         skipFiniteCheck=True,
                                                         clickable=True,
                                                         name=str(line_number))
        self.lines[line_number].sigClicked.connect(self.line_click)



    def remove_curve(self, line_number):
        self.lines[line_number].clear()
        # Force window activation so that I don't have to click the graph to gain focus and make it update
        self.activateWindow()
