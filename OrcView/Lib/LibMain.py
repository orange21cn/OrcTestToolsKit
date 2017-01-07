# coding=utf-8
from PySide.QtGui import QDockWidget
from PySide.QtGui import QTextEdit
from PySide.QtCore import QSize
from PySide.QtGui import QStyleOptionDockWidget
from PySide.QtCore import Signal as OrcSignal
from PySide.QtCore import QObject


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


class DockBottom(BaseDock):

    def __init__(self):

        BaseDock.__init__(self, 100)

        self.__win_log = QTextEdit()
        self.setWidget(self.__win_log)

        self.setFeatures(QDockWidget.DockWidgetClosable)
        # self.setStyleSheet(get_theme("dock"))

    def put_log(self, p_text):
        self.__win_log.insertHtml("%s<br>" % p_text)


def singleton(cls, *args, **kw):

    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class LogClient(QObject):

    sig_log = OrcSignal(str)

    def __init__(self):

        QObject.__init__(self)

    def put_message(self, p_text):
        self.sig_log.emit("<span style=\"color: green\">Message: %s</span>" % p_text)

    def put_error(self, p_text):
        self.sig_log.emit("<span style=\"color: red\">Error: %s</span>" % p_text)
