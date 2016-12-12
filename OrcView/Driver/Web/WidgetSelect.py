# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_widget_def

from WidgetService import WidgetDefService


class WidgetSelectModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)

        self.usr_set_service(WidgetDefService())


class WidgetSelectControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewWidgetSelect(QWidget):

    sig_selected = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        # Model
        self.__model = WidgetSelectModel()
        self.__model.usr_set_definition(def_view_widget_def)
        self.__model.usr_chk_able()

        # Control
        _control = WidgetSelectControl(def_view_widget_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_widget_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButtons([dict(id="search", name=u"查询")])

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)
        _wid_display.doubleClicked.connect(self.select)

    def search(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__model.usr_search(_cond)

    def select(self, p_index):
        _node = self.__model.usr_get_node(p_index).content
        _id = _node["id"]
        _path = _node["widget_path"]
        _type = _node["widget_type"]
        self.sig_selected.emit(dict(id=str(_id), flag=_path, type=_type))
        self.close()

    def __operate(self, p_flag):

        if "search" == p_flag:
            self.search()
        else:
            pass
