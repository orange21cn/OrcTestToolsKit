# coding=utf-8
from PySide.QtGui import QMenu
from PySide.QtGui import QAction
from PySide.QtGui import QCursor
from PySide.QtCore import Signal as OrcSignal

from functools import partial


class ViewContextMenu(QMenu):

    sig_clicked = OrcSignal(str)

    def __init__(self, p_def):
        """
        :param p_def: [{NAME:..., STR:...}, ...]
        :return:
        """
        QMenu.__init__(self)

        for _def in p_def:

            _act = QAction(_def["NAME"], self)
            _act.triggered.connect(partial(self.menu_emit, _def["STR"]))

            self.addAction(_act)

    def show_menu(self):
        self.popup(QCursor.pos())
        self.show()

    def menu_emit(self, p_str):
        self.sig_clicked.emit(p_str)
