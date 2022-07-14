import threading

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QDesktopWidget, QComboBox, QLabel, \
    QSlider, QRadioButton, QCheckBox
import logic
from loading_window import LoadingWindow
from table_window import TableWindow

start_window = None
table_window = None
word_count = 1
sort_type = "max"
column_index = 0
is_nearby = True


def get_column_names(df):
    names = []
    header_row = df.loc[0]

    for number in df.keys():
        names.append(chr(number + 65) + ") " + str(header_row[number]))

    return names


def set_word_count(count):
    global word_count
    word_count = count


def set_max_sort_type(status):
    global sort_type

    if status:
        sort_type = "max"


def set_min_sort_type(status):
    global sort_type

    if status:
        sort_type = "min"


def set_is_nearby(status):
    global is_nearby

    is_nearby = status


def get_phrases(df):
    global table_window

    df_without_header = logic.delete_header_row(df)
    client_sentences = logic.get_grouped_sentences(df_without_header, column_index)

    if is_nearby:
        phrases = logic.get_nearby_phrases(client_sentences, word_count)
    else:
        phrases = logic.get_outlying_phrases(client_sentences, word_count)

    phrase_count = logic.get_phrase_count_dict(phrases)
    sorted_phrases = logic.sort_phrases(phrase_count, sort_type)

    return sorted_phrases


def set_label_value(label, value):
    label.setText(str(value))


def SortWindow(back_window, df):
    global start_window
    start_window = back_window

    window = QMainWindow()

    window.setWindowTitle("Super sort app")
    window.setFixedSize(QSize(1000, 650))
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())

    column_text = QLabel(window)
    column_text.setText("Выберете колонку")
    column_text.move(310, 30)
    column_text.setStyleSheet("font-size: 25px")
    column_text.adjustSize()

    column_names = get_column_names(df)

    combo = QComboBox(window)
    combo.setFixedSize(QSize(350, 65))
    combo.move(310, 80)
    combo.setStyleSheet("QComboBox"
                        "{"
                        "border: 3px solid #27AE61;"
                        "border-radius: 13px;"
                        "font-size: 22px;"
                        "padding-left: 10px;"
                        "}"
                        "QComboBox::drop-down { "
                        "border: none"
                        "}"
                        "QComboBox QAbstractItemView { "
                        "font-size: 22px;"
                        "border: 3px solid #27AE61;"
                        "selection-background-color: #27AE61;"
                        "}"
                        "QComboBox QAbstractItemView::item { "
                        "border-radius: 13px;"
                        "padding: 20px;"
                        "min-height: 50px"
                        "}"
                        )

    combo.addItems(column_names)

    def set_column_index():
        global column_index
        column_index = combo.currentIndex()

    if len(column_names) > 7:
        combo.setCurrentIndex(7)
        set_column_index()

    combo.currentTextChanged.connect(set_column_index)

    sld_text = QLabel(window)
    sld_text.setText("Количество слов")
    sld_text.move(310, 200)
    sld_text.setStyleSheet("font-size: 25px")
    sld_text.adjustSize()

    sld = QSlider(Qt.Horizontal, window)
    sld.setFocusPolicy(Qt.NoFocus)
    sld.setFixedSize(QSize(350, 40))
    sld.setRange(1, 6)
    sld.setValue(1)
    sld.move(310, 250)
    sld.setStyleSheet("QSlider::handle:horizontal {"
                      "border-radius: 15px;"
                      "width: 30px;"
                      "margin-top: -15px;"
                      "background: #27AE61;"
                      "}")

    sld_value_text = QLabel(window)
    sld_value_text.setText("1")
    sld_value_text.move(680, 250)
    sld_value_text.setStyleSheet("font-size: 22px")
    sld_value_text.adjustSize()

    def change_word_count(count):
        set_label_value(sld_value_text, count)
        set_word_count(count)

    sld.valueChanged[int].connect(change_word_count)

    radiobutton_text = QLabel(window)
    radiobutton_text.setText("Cортировать по")
    radiobutton_text.move(310, 350)
    radiobutton_text.setStyleSheet("font-size: 25px")
    radiobutton_text.adjustSize()

    radiobutton_max = QRadioButton("Max", window)
    radiobutton_max.value = "Max"
    radiobutton_max.setChecked(True)
    radiobutton_max.move(310, 400)
    radiobutton_max.setStyleSheet(
        "QRadioButton {"
        "font-size: 22px"
        "}"
        "QRadioButton::indicator:unchecked {"
        "border: 3px solid #27AE61;"
        "min-width: 30;"
        "min-height: 30"
        "}"
        "QRadioButton::indicator:checked"
        "{"
        "background: #27AE61;"
        "min-width: 30;"
        "min-height: 30"
        "}")
    radiobutton_max.toggled.connect(set_max_sort_type)

    radiobutton_min = QRadioButton("Min", window)
    radiobutton_min.value = "Min"
    radiobutton_min.move(520, 400)
    radiobutton_min.setStyleSheet(
        "QRadioButton {"
        "font-size: 22px"
        "}"
        "QRadioButton::indicator:unchecked {"
        "border: 3px solid #27AE61;"
        "min-width: 30;"
        "min-height: 30"
        "}"
        "QRadioButton::indicator:checked"
        "{"
        "background: #27AE61;"
        "min-width: 30;"
        "min-height: 30"
        "}")
    radiobutton_min.toggled.connect(set_min_sort_type)

    checkbox = QCheckBox('Рядом стоящие', window)

    checkbox.move(310, 470)
    checkbox.setFixedSize(QSize(300, 30))

    checkbox.setStyleSheet(
        "QCheckBox {"
        "font-size: 22px"
        "}"
        "QCheckBox::indicator:unchecked {"
        "border: 3px solid #27AE61;"
        "min-width: 30;"
        "min-height: 30"
        "}"
        "QCheckBox::indicator:checked"
        "{"
        "background: #27AE61;"
        "min-width: 30;"
        "min-height: 30"
        "}")

    checkbox.setChecked(True)

    checkbox.toggled.connect(set_is_nearby)

    # -------------------------------------------------------------------------
    btn_search = QPushButton(window)
    btn_search.move(450, 540)
    btn_search.setText("Поиск")

    def search_btn_click():
        global table_window

        window.close()
        loading = LoadingWindow()
        loading.show()

        phrases = get_phrases(df)

        table_window = TableWindow(back_window, phrases[:1000])
        table_window.show()

    btn_search.clicked.connect(search_btn_click)

    btn_search.setFixedSize(QSize(100, 55))
    btn_search.setStyleSheet("background: #27AE61;"
                             "border-radius: 13%;"
                             "font-size: 25px;"
                             "color: #FFF")

    btn_back = QPushButton(window)
    btn_back.move(870, 540)
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

    return window
