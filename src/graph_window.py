"""Detailed plot of a byte

Generate a detailed plot of a single byte with a list of checkboxes to choose which lines to plot.
Show by default only the one line with the peak.
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox
import csv

GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = '../data/output/npy/'
PEAKS_CSV = '../data/output/csv/peaks.csv'


class GraphWindow(QtWidgets.QMainWindow):
    """Window containing a plot of a byte and a selector for the lines to plot."""

    # Create a custom signal with corresponding arguments
    message = pyqtSignal(int, float, str)

    def __init__(self, *args, **kwargs):
        """Class constructor."""
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi(GRAPH_WINDOW_UI, self)
        self.correlation_values = None
        self.lines = None
        self.peak_line = None
        self.vbox = None
        self.pushButton.clicked.connect(self.clear_checks)
        self.message.connect(self.msg_callback)

        # Cursor position
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.graph_widget.addItem(self.vLine, ignoreBounds=True)
        self.graph_widget.addItem(self.hLine, ignoreBounds=True)
        self.graph_widget.scene().sigMouseMoved.connect(self.mouse_moved)

    def mouse_moved(self, event):
        mouse_point = self.graph_widget.mapToView(event)
        self.vLine.setPos(mouse_point.x())
        self.hLine.setPos(mouse_point.y())
        self.mouse_position_label.setText(f'x={int(mouse_point.x())}, y={mouse_point.y():.3f}')

    def msg_callback(self, x, y, line):
        print(f"Custom signal received with values x = {x}, y = {y} and line number {line}")

    def line_click(self, item, points):
        """Print the coordinates of the point on the plot which is clicked by the user."""
        x = int(np.floor(points.pos().x()))
        y = self.correlation_values[:, int(item.name())][x]
        self.message.emit(x, y, item.name())
        print(f'Line number {item.name()} clicked on (x={x}, y={y:.3f})')

    def init_empty_plot(self, byte_number):
        """Initialize an empty plot of a byte where only the peak is highlighted."""
        try:
            self.correlation_values = np.load(f'{NPY_DIRECTORY}{str(byte_number).zfill(2)}.npy', mmap_mode='r')
        except FileNotFoundError:
            print('[ERROR] .npy file not found. Run the two initial scripts before.')
            exit()

        self.lines = [None] * self.correlation_values.shape[1]

        # Plot only data points that are currently visible (smooth when zoomed in)
        self.graph_widget.setClipToView(True)

        # Enable downsampling with:
        # - auto=True (automatically pick reduction factor for the visible samples based on visible range)
        # - mode='subsample' (fastest but least accurate method)
        self.graph_widget.setDownsampling(auto=True, mode='peak')

        try:
            with open(PEAKS_CSV) as peaks_file:
                csv_reader = csv.reader(peaks_file)
                csv_rows = list(csv_reader)
                self.peak_line = int(csv_rows[byte_number][0])
                peak_x = int(csv_rows[byte_number][1])
                peak_y = float(csv_rows[byte_number][2])

                text = pg.TextItem(
                    html='<div style="text-align: center"><span style="color: #FFF;">Peak value',
                    anchor=(-0.3, 0.5), angle=0, border='w', fill=(0, 0, 255, 100))
                self.graph_widget.addItem(text)
                text.setPos(peak_x, peak_y)

                arrow = pg.ArrowItem(pos=(peak_x, peak_y), angle=0)
                self.graph_widget.addItem(arrow)

            label_content = 'WARNING! This file contains only NaN values.' if self.peak_line == -1 \
                else f'The peak is in correspondence of curve {self.peak_line}.'

            self.info_label.setText(label_content)

        except FileNotFoundError:
            print('[ERROR] peaks.csv file not found. Run the two initial scripts before.')
            exit()

    def create_scrollarea(self):
        """Create the scrollArea with the checkboxes to control the lines to plot, and check the line with the peak."""
        self.vbox = QVBoxLayout()

        for line_num in range(self.correlation_values.shape[1]):
            checkbox = QCheckBox(f'curve {line_num}')
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
        """Add a curve when a checkbox is checked, and remove a checkbox when a checkbox is unchecked."""
        if state == QtCore.Qt.Checked:
            self.add_curve(curve_number)
        else:
            self.remove_curve(curve_number)

    def clear_checks(self):
        """Clear all the checks from the checkboxes in the scrollArea."""
        for i in range(self.correlation_values.shape[1]):
            checkbox = self.vbox.itemAt(i).widget()
            if checkbox.isChecked:
                checkbox.setChecked(False)

    def add_curve(self, line_number):
        """Plot one of the lines of a byte."""
        self.lines[line_number] = self.graph_widget.plot(self.correlation_values[:, line_number],
                                                         pen=pg.intColor(line_number),
                                                         skipFiniteCheck=True,
                                                         clickable=True,
                                                         name=str(line_number))
        self.lines[line_number].sigClicked.connect(self.line_click)

    def remove_curve(self, line_number):
        """Delete the plot of one line of a byte."""
        self.lines[line_number].clear()
        # Plot a "dumb" point so that the widget is refreshed and the removed curve is disappeared
        self.graph_widget.plot([0], [0])
