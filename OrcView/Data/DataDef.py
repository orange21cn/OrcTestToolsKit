# coding=utf-8

from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibViewDef import view_data_def

from OrcView.Lib.LibTable import ModelNewTable
from OrcView.Lib.LibControl import LibControl

from DataService import DataService


class DataModel(ModelNewTable):

    def __init__(self):

        ModelNewTable.__init__(self)

        service = DataService()
        self.usr_set_service(service)


class DataControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewDataMag(QWidget):
    """
    View of table
    """
    def __init__(self):

        QWidget.__init__(self)

        self.title = u"数据管理"

        # Model
        self.__model = DataModel()
        self.__model.usr_set_definition(view_data_def)

        # Control
        _control = DataControl(view_data_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(view_data_def)
        self.__wid_search_cond.set_col_num(3)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_modify()
        _wid_buttons.enable_search()
        _wid_buttons.create()

        # win_add
        self.__win_add = ViewAdd(view_data_def)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.__win_add.show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)
        _wid_buttons.sig_search.connect(self.search)

        self.__win_add.sig_submit[dict].connect(self.add)

    def search(self):
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        self.__model.usr_add(p_data)
