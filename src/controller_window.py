import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox

CONTROLLER_WINDOW_UI = 'ui/controller_window.ui'


class ControllerWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ControllerWindow, self).__init__(*args, **kwargs)
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
            self.vbox.addWidget(checkbox)

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)
        self.setGeometry(600, 100, 300, 550)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ControllerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
