import pandas as pd
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QDesktopWidget, QFileDialog
from sort_window import SortWindow

sort_window = None


def get_data_from_xlsx(filepath):
    excel_data = pd.read_excel(filepath, header=None)
    return pd.DataFrame(excel_data)


def choose_file(window):
    global sort_window

    file_dialog = QFileDialog()
    file_dialog.setNameFilters(["XLSX files (*.xlsx)"])
    file_dialog.selectNameFilter("XLSX files (*.xlsx)")

    filepath = file_dialog.getOpenFileName()[0]

    if filepath and filepath.split(".")[-1] == "xlsx":
        df = get_data_from_xlsx(filepath)
        sort_window = SortWindow(window, df)
        sort_window.show()
        window.close()


def StartWindow():
    window = QMainWindow()

    window.setWindowTitle("Super sort app")
    window.setFixedSize(QSize(500, 300))
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())

    btn = QPushButton(window)
    btn.move(100, 110)
    btn.setText("+      Выбрать файл")

    def btn_click():
        choose_file(window)

    btn.clicked.connect(btn_click)

    btn.setFixedSize(QSize(300, 75))
    btn.setStyleSheet("background: #27AE61;"
                      "border-radius: 13%;"
                      "font-size: 25px;"
                      "color: #FFF")

    return window
