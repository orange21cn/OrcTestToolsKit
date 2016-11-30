# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTable import ModelNewTable
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import def_view_page_def

from PageService import PageDefService


class PageSelectModel(ModelNewTable):

    def __init__(self):

        ModelNewTable.__init__(self)

        self.usr_set_service(PageDefService())


class PageSelectControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewPageSelectMag(QWidget):

    sig_selected = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"用例管理"

        # Model
        self.__model = PageSelectModel()
        self.__model.usr_set_definition(def_view_page_def)

        # Control
        _control = PageSelectControl(def_view_page_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_page_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButtons([dict(id="search", name=u"查询")])

        # win_add
        self.__win_add = ViewAdd(def_view_page_def)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)
        _wid_display.doubleClicked.connect(self.select)

    def __operate(self, p_flag):

        if "search" == p_flag:
            self.search()
        else:
            pass

    def search(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__model.usr_search(_cond)

    def select(self, p_index):

        _node = self.__model.usr_get_data(p_index.row())
        _id = _node["id"]
        _flag = _node["page_flag"]

        self.sig_selected.emit(dict(id=str(_id), flag=_flag))

        self.close()
