# coding=utf-8
from PySide.QtGui import QDockWidget
from PySide.QtGui import QTextEdit
from PySide.QtCore import Qt
from PySide.QtCore import QSize
from PySide.QtCore import Signal as OrcSignal
from PySide.QtCore import QObject

from OrcLib.LibProgram import orc_singleton
from OrcView.Lib.LibTheme import get_theme


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


@orc_singleton
class DockLog(BaseDock):

    def __init__(self):

        BaseDock.__init__(self, 50)

        self.__win_log = QTextEdit()
        self.__win_log.setReadOnly(True)
        self.__win_log.setMinimumHeight(10)
        self.__win_log.setMaximumHeight(100)
        self.setWindowTitle("Log")
        self.setWidget(self.__win_log)

        self.setFeatures(QDockWidget.DockWidgetVerticalTitleBar | QDockWidget.DockWidgetClosable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # self.setStyleSheet(get_theme("dock"))

        log_client = LogClient()
        log_client.sig_log.connect(self.put_log)

        self.setStyleSheet(get_theme('DockBottom'))

    def put_log(self, p_text):
        self.__win_log.insertHtml("%s<br>" % p_text)


@orc_singleton
class LogClient(QObject):

    sig_log = OrcSignal(str)

    def __init__(self):

        QObject.__init__(self)

    def debug(self, p_msg):
        self.sig_log.emit("<span style=\"color: green\">Debug: %s</span>" % p_msg)

    def info(self, p_msg):
        self.sig_log.emit("<span style=\"color: green\">Info: %s</span>" % p_msg)

    def warning(self, p_msg):
        self.sig_log.emit("<span style=\"color: orange\">Warning: %s</span>" % p_msg)

    def error(self, p_msg):
        self.sig_log.emit("<span style=\"color: red\">Error: %s</span>" % p_msg)

    def critical(self, p_msg):
        self.sig_log.emit("<span style=\"color: red\">Critical: %s</span>" % p_msg)
