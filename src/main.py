"""
Entry point for the program.
"""


import sys
from PyQt5 import QtWidgets
import main_window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = main_window.MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

