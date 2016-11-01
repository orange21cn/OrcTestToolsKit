# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelNewTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import LibControl

from service import WindowService


class WindowModel(ModelNewTable):

    def __init__(self):

        ModelNewTable.__init__(self)

        service = WindowService()
        self.usr_set_interface(service)


class WindowControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewWindow(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="window_flag", NAME=u"窗口标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="window_mark", NAME=u"标识控件", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="window_desc", NAME=u"窗口描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        # Current window id
        self.__window_id = None

        # Model
        self.__model = WindowModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = WindowControl(_table_def)

        # Data result display window
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Search condition
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Buttons window
        _btn_definition = [
            dict(id="refresh", name=u'刷新'),
            dict(id="search", name=u"查询"),
            dict(id="update", name=u"修改"),
            dict(id="delete", name=u"删除")
        ]
        _wid_buttons = ViewButtons(_btn_definition)
        _wid_buttons.align_back()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

    def __operate(self, p_flg):

        if "search" == p_flg:
            _cond = self.__wid_search_cond.get_cond()
            self.__model.usr_search(_cond)
        elif "refresh" == p_flg:
            self.__model.usr_add(None)
        elif "update" == p_flg:
            self.__model.usr_editable()
        elif "delete" == p_flg:
            self.__model.usr_delete()
        else:
            pass

    def set_window_id(self, p_window_id):
        self.__window_id = p_window_id
        self.__model.usr_search({"window_id": self.__window_id})

    def clean(self):
        self.__window_id = None
        self.__model.usr_clean()
