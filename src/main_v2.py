import sys
from PyQt5 import QtWidgets, uic


UI_FILE = 'ui/mainwindow_buttons.ui'
NPY_DIRECTORY = "../sample_data/npy/"


class GraphWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 2")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graph_window = None
        uic.loadUi(UI_FILE, self)
        self.create_buttons()

    def create_buttons(self):

        for i in range(4):
            for j in range(4):
                button = QtWidgets.QPushButton("test")
                button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.gridLayout.addWidget(button, i, j)

                button.setToolTip("click to show the plot")
                button.clicked.connect(self.spawn_window)

    def spawn_window(self):
        self.graph_window = GraphWindow()
        self.graph_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Rendering the window...')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
