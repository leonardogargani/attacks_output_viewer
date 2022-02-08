"""
Main window of the program.
Create a button for each CSV file that is found. If clicked, the button shows a plot.
"""


import os
from PyQt5 import QtWidgets, uic
import graph_window


MAIN_WINDOW_UI = 'ui/main_window.ui'
GRAPH_WINDOW_UI = 'ui/graph_window.ui'
NPY_DIRECTORY = "../data/output/npy/"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.secondary_window = None
        uic.loadUi(MAIN_WINDOW_UI, self)
        self.create_buttons()

    # overriding the closeEvent default function
    def closeEvent(self, event):
        self.secondary_window.close()

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
        self.secondary_window = graph_window.GraphWindow()
        self.secondary_window.top_label.setText("Byte #" + str(byte_number).zfill(2))
        self.secondary_window.generate_plot(byte_number)
        self.secondary_window.show()
