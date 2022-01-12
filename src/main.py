"""Main window of the program

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
INPUT_FOLDER = "../sample_data/"

# ======================================================================================================================
# If not already done, convert csv files to npy format and save them
for i in range(16):
    filename = 'data_byte_' + str(i).zfill(2)
    if not os.path.exists(INPUT_FOLDER + filename + '.npy'):
        # Read csv file
        correlation_values = np.loadtxt(INPUT_FOLDER + filename + '.csv', delimiter=',')
        print('Loading ' + filename + '...')
        # Save to npy format
        np.save(INPUT_FOLDER + filename, correlation_values)

# Special case for the data from the professor
filename = '1'
if not os.path.exists(INPUT_FOLDER + filename + '.npy'):
    # Read csv file
    # !!! WARNING !!! Delimiter is now a space character and not a comma. The nan values are replaced by 0
    correlation_values = np.genfromtxt(INPUT_FOLDER + filename + '.csv', delimiter=' ', filling_values=0)
    # Save to npy format
    # Saving it 16 times while waiting for the full data set
    for i in range(16):
        np.save(INPUT_FOLDER + f'{i}', correlation_values)
# ======================================================================================================================



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(UI_FILE, self)
        self.populate_menubar()
        # plot the first byte by default
        self.plot_byte(0)

    def populate_menubar(self):
        filenames = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv')]
        for filename in sorted(filenames):
            action = QtWidgets.QAction(filename, self)
            byte_num = int(filename.partition('.')[0][-2:])
            # due to python's scoping rules and closures, we need to capture byte_num
            action.triggered.connect(lambda state, x=byte_num: self.plot_byte(x))
            self.menuSelect.addAction(action)

    def plot_byte(self, byte_number):
        start = time.time()
        # For generated by us csv files
        #filename = 'data_byte_' + str(byte_number).zfill(2) + '.csv'
        #correlation_values = np.loadtxt(INPUT_FOLDER + filename, delimiter=',')

        # For converted npy files generated by us
        #correlation_values = np.load(INPUT_FOLDER + 'data_byte_' + str(byte_number).zfill(2) + '.npy')

        # For real csv file
        #correlation_values = np.genfromtxt(INPUT_FOLDER + '1.csv', delimiter=' ', filling_values=0)

        # For real converted file to npy
        correlation_values = np.load(INPUT_FOLDER + f'{byte_number+1}.npy')

        dt = time.time() - start
        print('File loaded in', dt, 'seconds')

        start = time.time()
        for num in range(correlation_values.shape[1]):
            # Plot only data points that are currently visible
            # When plot is zoomed, less points are plotted and therefore it is smoother
            self.graph_widget.setClipToView(True)
            # Enable downsampling
            # ds = 0.1 is a dummy value because auto is set to True and therefore ds is automatically picked in function of visible range
            # mode='subsample', least accurate method but fast
            # see documentation for more details https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
            self.graph_widget.setDownsampling(ds=0.1, auto=True, mode='subsample')
            # Disable auto range before plotting for faster plots
            self.graph_widget.disableAutoRange()
            # Plot
            # see https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotdataitem.html
            # connecting all the lines helps speed up the plot time
            # skipFiniteCheck is by default False, we set it to True because we know that no NaN values are in our data this help speed up plot time
            # According to the doc but no obvious change detected, I am probably not using these features in the correct way
            # The argument clickable=True makes the curve clickable and when clicked the signal sigClicked is emitted but I don't know how to catch that signal
            # Here is the doc sigClicked https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotcurveitem.html
            self.graph_widget.plot(correlation_values[:, num], pen=pg.intColor(num), skipFiniteCheck=True, connect='all', clickable=True)
            # Enable auto range
            self.graph_widget.autoRange()

        dt = time.time() - start
        print(f'Plot generated in {dt} seconds')

        # We don't use the array anymore so we free the variable
        correlation_values = None

        self.top_label.setText("Byte #" + str(byte_number).zfill(2))


def main():
    ## Switch to using white background and black foreground
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Rendering the window...')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
