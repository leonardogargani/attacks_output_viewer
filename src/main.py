"""
This file starts the program and shows one plot at a time.
The byte to be shown can be selected through a dropdown menu.
"""

import os
import sys
import time

from PyQt5 import QtWidgets, uic
import numpy as np
import pyqtgraph as pg

UI_FILE = 'ui/mainwindow.ui'
NPY_DIRECTORY = "../sample_data/npy/"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(UI_FILE, self)
        self.populate_menubar()
        # plot the first byte by default
        self.plot_byte(1)

    def populate_menubar(self):
        filenames = [f for f in os.listdir(NPY_DIRECTORY) if f.endswith('.npy')]
        for filename in sorted(filenames):
            action = QtWidgets.QAction(filename, self)
            byte_num = int(os.path.splitext(filename)[0])
            # due to python's scoping rules and closures, we need to capture byte_num
            action.triggered.connect(lambda state, x=byte_num: self.plot_byte(x))
            self.menuSelect.addAction(action)

    def click(self, mouseClickEvent):
        # TODO: investigate mouseClickEvent method, such as getData etc...
        print('mouse click')

    def plot_byte(self, byte_number):
        start = time.time()
        correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy')
        dt = time.time() - start
        print('File to plot loaded in ' + str(dt) + ' seconds')

        print('Generating the plot...')
        start = time.time()

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

            # TODO: doc for sigClicked https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotcurveitem.html
            line.sigClicked.connect(self.click)

            # re-enable auto range
            self.graph_widget.autoRange()

        dt = time.time() - start
        print('Plot generated in ' + str(dt) + ' seconds')

        self.top_label.setText("Byte #" + str(byte_number).zfill(2))


def main():
    # use white background and black foreground
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    pg.setConfigOptions(antialias=True)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Rendering the window...')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
