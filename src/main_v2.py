"""


"""

import os
import sys

from PyQt5 import QtWidgets, uic


UI_FILE = 'ui/mainwindow_buttons.ui'
NPY_DIRECTORY = "../sample_data/npy/"


class GraphWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graph_window = None
        uic.loadUi(UI_FILE, self)
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
        self.graph_window.show()
        self.graph_window.setWindowTitle('Byte ' + str(byte_number))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Rendering the window...')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
