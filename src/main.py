"""Main window of the program

This file starts the program and shows one plot at a time.
The byte to be shown can be selected through a dropdown menu.
"""

from PyQt5 import QtWidgets, uic
import numpy as np
import sys

UI_FILE = 'ui/mainwindow.ui'
INPUT_FOLDER = "../sample_data/"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(UI_FILE, self)
        # start by plotting the first byte
        self.plot_byte(1)

    def plot_byte(self, byte_number):
        filename = 'data_byte_' + str(byte_number).zfill(2) + '.csv'

        correlation_values = np.loadtxt(INPUT_FOLDER + filename, delimiter=',')
        print('Loading ' + filename + '...')

        time_instants = range(correlation_values.shape[0])

        for num in range(correlation_values.shape[1]):
            self.graph_widget.plot(time_instants, correlation_values[:, num])

        self.top_label.setText("Byte #" + str(byte_number))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Rendering the window...')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
