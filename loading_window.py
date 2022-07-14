from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow


def LoadingWindow():
    window = QMainWindow()

    window.setWindowTitle("Обработка...")
    window.setFixedSize(QSize(500, 10))
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())

    return window
