from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox

CONTROLLER_WINDOW_UI = 'ui/controller_window.ui'


class ControllerWindow(QtWidgets.QMainWindow):

    def __init__(self, graph_window):
        super(ControllerWindow, self).__init__()
        self.graph_window = graph_window
        self.vbox = None
        self.widget = None
        uic.loadUi(CONTROLLER_WINDOW_UI, self)
        self.pushButton.clicked.connect(self.clear_checks)

    def create_scrollarea(self):
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        for i in range(256):
            checkbox = QCheckBox("curve " + str(i))
            checkbox.stateChanged.connect(lambda state, x=i: self.click_checkbox(state, x))
            # at first, check only the line with the peak
            if i == self.graph_window.peak_line:
                checkbox.setChecked(True)
            self.vbox.addWidget(checkbox)

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)

    def click_checkbox(self, state, curve_number):
        if state == QtCore.Qt.Checked:
            print('Checked ' + str(curve_number))
            self.graph_window.add_curve(curve_number)
        else:
            print('self.graph_window.peak_line = ' + str(self.graph_window.peak_line))

            print('Unchecked ' + str(curve_number))
            self.graph_window.remove_curve(curve_number)

    def clear_checks(self):
        for i in range(256):
            checkbox = self.vbox.itemAt(i).widget()
            if checkbox.isChecked:
                checkbox.setChecked(False)

        self.graph_window.activateWindow()
