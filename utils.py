import os
from datetime import date, datetime

import mysql.connector

from hijri_converter import Hijri, Gregorian
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from PyQt5.QtWidgets import (QApplication,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
                             QMainWindow,
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSlider,
                             QSpinBox,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget,
                             QHBoxLayout,
                             QGridLayout,
                             QTableWidget,
                             QHeaderView, QMenu, QAction, QInputDialog, QFormLayout, QDialogButtonBox, QDialog
                             )
from PyQt5.QtGui import (QPalette,
                         QColor,
                         QFont,
                         )

import sys
from random import choice

class Box(QWidget):

    def __init__(self, color):
        super(Box, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.init_ui()

    def init_ui(self):
        self.show()


class errPopup(QWidget):
    def __init__(self,code):
        super().__init__()

        self.layout = QHBoxLayout()

        self.error = "Error code: " + code
        self.label = QLabel(self.error)
        self.button = QPushButton("OK")
        self.button.clicked.connect(self.close)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


connection = mysql.connector.connect(
    # trail3server.mysql.database.azure.com
    # host="trail3server.mysql.database.azure.com",
    # user="sehran",
    # passwd="Noor123!@",
    # port=3306,
    host= "localhost",
    user="root",
    passwd="Somsoc1retupmoc",
    port=3306,
    database='sugarBilling'
)


