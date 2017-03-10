# coding=utf-8
from PySide.QtGui import QPushButton
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget


class ViewCheck(QWidget):
    """

    """
    def __init__(self):

        QWidget.__init__(self)

        self.__test = QPushButton("ViewCheck")

        _layout = QVBoxLayout()
        self.setLayout(_layout)

        _layout.addWidget(self.__test)