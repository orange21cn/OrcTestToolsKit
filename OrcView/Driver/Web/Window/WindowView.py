# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import def_view_window_def

from .WindowModel import WindowModel


class WindowControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'Window')


class WindowView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"窗口"

        # Current window id
        self.__window_id = None

        # Data result display window
        self.display = ViewTable('Window', WindowModel, WindowControl)

        # Search condition
        self.__wid_search_cond = ViewSearch(def_view_window_def)
        self.__wid_search_cond.set_col_num(3)
        self.__wid_search_cond.create()

        # Buttons window
        btn_definition = [
            dict(id="refresh", name=u'刷新'),
            dict(id="search", name=u"查询"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="delete", name=u"删除")
        ]
        wid_buttons = OrcButtons(btn_definition)
        wid_buttons.align_back()

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 点击按钮操作
        wid_buttons.sig_clicked.connect(self.operate)

    def operate(self, p_flg):
        """
        点击按钮操作
        :param p_flg:
        :return:
        """
        if "search" == p_flg:
            _cond = self.__wid_search_cond.get_cond()
            self.display.model.mod_search(_cond)
        elif "refresh" == p_flg:
            self.display.model.mod_add(None)
        elif "update" == p_flg:
            self.display.model.editable()
        elif "delete" == p_flg:
            self.display.model.mod_delete()
        else:
            pass

    def set_window_id(self, p_window_id):
        self.__window_id = p_window_id
        self.display.model.mod_search({"window_id": self.__window_id})

    def clean(self):
        self.__window_id = None
        self.display.model.mod_clean()
