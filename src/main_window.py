"""Main window of the program

Create a button for each CSV file that is found. If clicked, the button shows a detailed plot.
"""


import os
from PyQt5 import QtWidgets, uic

import graph_window

MAIN_WINDOW_UI = 'ui/main_window.ui'
NPY_DIRECTORY = "../data/output/npy/"


class MainWindow(QtWidgets.QMainWindow):
    """Window containing all the buttons to plot each one of the bytes."""

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graph_windows = []
        uic.loadUi(MAIN_WINDOW_UI, self)
        self.create_buttons()

    # Override the closeEvent function to close also all the graph windows
    def closeEvent(self, event):
        """Close all the windows with plots when the current window is closed (override default closeEvent function)."""
        if self.graph_windows:
            for window in self.graph_windows:
                window.close()

    def create_buttons(self):
        """Create a matrix of buttons (that plot bytes), each one for every npy file corresponding to a byte."""
        filenames = [f for f in os.listdir(NPY_DIRECTORY) if f.endswith('.npy')]
        row_index = 0
        column_index = 0
        for filename in sorted(filenames):
            byte_num = int(os.path.splitext(filename)[0])

            button = QtWidgets.QPushButton(f'Byte {byte_num}')
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            button.setToolTip('click to show the plot')
            # Due to python's scoping rules and closures, we need to capture byte_num
            button.clicked.connect(lambda state, x=byte_num: self.plot_byte(x))

            self.gridLayout.addWidget(button, row_index, column_index)

            # Place the buttons in rows of 4 elements
            if (column_index % 3 == 0) and (column_index != 0):
                row_index += 1
                column_index = 0
            else:
                column_index += 1

    def plot_byte(self, byte_number):
        """Plot a byte in a new window."""
        window = graph_window.GraphWindow()
        window.byte_label.setText(f'Byte #{str(byte_number).zfill(2)}')
        window.init_empty_plot(byte_number)
        window.create_scrollarea()
        window.show()
        self.graph_windows.append(window)

