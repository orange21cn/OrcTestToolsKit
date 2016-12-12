# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_window_def

from WindowService import WindowDefService


class WindowModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        self.usr_set_service(WindowDefService())


class WindowControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewWindow(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"窗口"

        # Current window id
        self.__window_id = None

        # Model
        self.__model = WindowModel()
        self.__model.usr_set_definition(def_view_window_def)

        # Control
        _control = WindowControl(def_view_window_def)

        # Data result display window
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Search condition
        self.__wid_search_cond = ViewSearch(def_view_window_def)
        self.__wid_search_cond.set_col_num(3)
        self.__wid_search_cond.create()

        # Buttons window
        _btn_definition = [
            dict(id="refresh", name=u'刷新'),
            dict(id="search", name=u"查询"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="delete", name=u"删除")
        ]
        _wid_buttons = ViewButtons(_btn_definition)
        _wid_buttons.align_back()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

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
