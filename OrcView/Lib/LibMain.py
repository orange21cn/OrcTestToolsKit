# coding=utf-8
from PySide.QtGui import QDockWidget
from PySide.QtGui import QTextEdit
from PySide.QtCore import QSize


class BaseDock(QDockWidget):

    def __init__(self, p_size):
        QDockWidget.__init__(self)

        self.__size = p_size

    def sizeHint(self):
        return QSize(self.__size, self.__size)


class DockCategory(BaseDock):

    def __init__(self):
        BaseDock.__init__(self, 150)


class DockDetail(BaseDock):

    def __init__(self):
        BaseDock.__init__(self, 150)

    def show_detail(self):
        pass

    def display(self):
        pass

    def close_detail(self):
        pass


class DockLog(BaseDock):

    def __init__(self):
        BaseDock.__init__(self, 100)

        self.ttt = QTextEdit()
        self.setWidget(self.ttt)

    def set_log(self, p_text):
        self.ttt.setText(p_text)