"""Controller for the detailed plot
Create a controller where each checkbox shows/hides a single line in the detailed plot.
"""

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox


CONTROLLER_WINDOW_UI = 'ui/controller_window.ui'


class ControllerWindow(QtWidgets.QMainWindow):

    def __init__(self, graph_window):
        super(ControllerWindow, self).__init__()
        uic.loadUi(CONTROLLER_WINDOW_UI, self)
        self.graph_window = graph_window
        self.vbox = None
        self.pushButton.clicked.connect(self.clear_checks)

    # the line with the peak is created by this function
    def create_scrollarea(self):
        self.vbox = QVBoxLayout()

        for line_num in range(256):
            checkbox = QCheckBox("curve " + str(line_num))
            checkbox.stateChanged.connect(lambda state, x=line_num: self.click_checkbox(state, x))
            # At first, check only the line with the peak
            if line_num == self.graph_window.peak_line:
                checkbox.setChecked(True)
            self.vbox.addWidget(checkbox)

        widget = QWidget()
        widget.setLayout(self.vbox)
        self.scrollArea.setWidget(widget)

    def click_checkbox(self, state, curve_number):
        if state == QtCore.Qt.Checked:
            self.graph_window.add_curve(curve_number)
        else:
            self.graph_window.remove_curve(curve_number)

    def clear_checks(self):
        for i in range(256):
            checkbox = self.vbox.itemAt(i).widget()
            if checkbox.isChecked:
                checkbox.setChecked(False)

        self.graph_window.activateWindow()
