"""Detailed plot of a byte
Generate a detailed plot of a single byte with a list of checkboxes to choose which lines to plot.
Show by default only the one line with the peak.
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox
import csv

GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = "../data/output/npy/"


class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi(GRAPH_WINDOW_UI, self)
        self.correlation_values = None
        self.lines = [None] * 256
        self.peak_line = None
        self.vbox = None
        self.pushButton.clicked.connect(self.clear_checks)

    def line_click(self, item, points):
        print("Line number " + item.name() + " clicked on x = {:.3f} y = {:.3f}".format(points.pos().x(),
                                                                                        points.pos().y()))

    def init_empty_plot(self, byte_number):
        self.correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy', mmap_mode='r')

        # Plot only data points that are currently visible (smooth when zoomed in)
        self.graph_widget.setClipToView(True)

        # Enable downsampling with:
        # - auto=True (automatically pick reduction factor for the visible samples based on visible range)
        # - mode='subsample' (fastest but least accurate method)
        self.graph_widget.setDownsampling(auto=True, mode='peak')

        with open('../data/output/csv/peak.csv') as peaks_file:
            csv_reader = csv.reader(peaks_file)
            csv_rows = list(csv_reader)
            self.peak_line = int(csv_rows[byte_number][0])
            peak_x = int(csv_rows[byte_number][1])
            peak_y = float(csv_rows[byte_number][2])

        # Highlight peak with two lines and a circle
        self.graph_widget.addLine(x=peak_x)
        self.graph_widget.addLine(y=peak_y)
        self.graph_widget.plot([peak_x], [peak_y], symbol='o', symbolSize=15)

        label_content = 'WARNING! This file contains only NaN values.' if self.peak_line == -1 \
            else 'The peak is in correspondence of curve ' + str(self.peak_line) + '.'

        self.info_label.setText(label_content)
        self.create_scrollarea()
        self.show()

    # the line with the peak is created by this function
    def create_scrollarea(self):
        self.vbox = QVBoxLayout()

        for line_num in range(256):
            checkbox = QCheckBox("curve " + str(line_num))
            checkbox.stateChanged.connect(lambda state, x=line_num: self.click_checkbox(state, x))
            # At first, check only the line with the peak
            if line_num == self.peak_line:
                checkbox.setChecked(True)
            self.vbox.addWidget(checkbox)

        widget = QWidget()
        widget.setLayout(self.vbox)
        self.scrollArea.setWidget(widget)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def click_checkbox(self, state, curve_number):
        if state == QtCore.Qt.Checked:
            self.add_curve(curve_number)
        else:
            self.remove_curve(curve_number)

    def clear_checks(self):
        for i in range(256):
            checkbox = self.vbox.itemAt(i).widget()
            if checkbox.isChecked:
                checkbox.setChecked(False)

    def add_curve(self, line_number):
        self.lines[line_number] = self.graph_widget.plot(self.correlation_values[:, line_number],
                                                         pen=pg.intColor(line_number),
                                                         skipFiniteCheck=True,
                                                         clickable=True,
                                                         name=str(line_number))
        self.lines[line_number].sigClicked.connect(self.line_click)

    def remove_curve(self, line_number):
        self.lines[line_number].clear()
        # Plot a "dumb" point so that the widget is refreshed and the removed curve is disappeared
        self.graph_widget.plot([0], [0])
