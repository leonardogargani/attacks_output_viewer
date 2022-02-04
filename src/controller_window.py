import sys
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
        self.setWindowTitle('Graph controller')
        self.create_scrollarea()

    def create_scrollarea(self):
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        for i in range(256):
            checkbox = QCheckBox("curve " + str(i))
            checkbox.stateChanged.connect(lambda state, x=i: self.click_checkbox(state, x))
            self.vbox.addWidget(checkbox)

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)
        self.setGeometry(600, 100, 300, 550)

    def click_checkbox(self, state, curve_number):
        if state == QtCore.Qt.Checked:
            print('Checked ' + str(curve_number))
            self.graph_window.add_curve(curve_number)
        else:
            print('Unchecked ' + str(curve_number))
            self.graph_window.remove_curve(curve_number)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ControllerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
