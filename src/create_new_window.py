"""Demo of spawning new window

This script just shows how to spawn a new window upon a button press.
"""

import sys
from PyQt5 import QtWidgets, uic

UI_FILE = 'ui/mainwindow_buttons.ui'


class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 2")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.window2 = None
        uic.loadUi(UI_FILE, self)

        self.pushButton = QtWidgets.QPushButton("Click me", self)
        self.pushButton.setToolTip("open a second window")
        self.pushButton.clicked.connect(self.create_window2)

    def create_window2(self):
        self.window2 = Window2()
        self.window2.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
