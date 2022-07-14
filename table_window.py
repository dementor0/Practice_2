from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *


start_window = None
row = 1000
col = 2


def create_table(window, data):
    global row, col

    table = QTableWidget(window)
    table.setColumnCount(col)
    table.setRowCount(row)
    table.setHorizontalHeaderLabels(("Phrase", "Number"))
    table.setMinimumWidth(500)
    table.setMinimumHeight(800)
    table.setShowGrid(True)

    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    table.verticalHeader().hide()

    for i, item in enumerate(data):
        for j, val in enumerate(item):
            table.setItem(i, j, QTableWidgetItem(str(val)))

    table.show()


def TableWindow(back_window, data):
    global start_window
    start_window = back_window

    window = QMainWindow()

    window.setWindowTitle("Show Table")
    window.setFixedSize(QSize(500, 900))

    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())

    btn_back = QPushButton(window)
    btn_back.move(390, 835)
    btn_back.setText("Меню")

    def back_btn_click():
        start_window.show()
        window.close()

    btn_back.clicked.connect(back_btn_click)

    btn_back.setFixedSize(QSize(100, 55))
    btn_back.setStyleSheet("background: #27AE61;"
                           "border-radius: 13%;"
                           "font-size: 25px;"
                           "color: #FFF")

    create_table(window, data)

    return window
