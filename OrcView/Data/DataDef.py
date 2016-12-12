# coding=utf-8

from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibViewDef import def_view_data

from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import LibControl

from DataService import DataService


class DataModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

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
        self.__model.usr_set_definition(def_view_data)

        # Control
        _control = DataControl(def_view_data)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_data)
        self.__wid_search_cond.set_col_num(3)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="search", name=u"查询")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_data)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

        self.__win_add.sig_submit[dict].connect(self.add)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "update" == p_flag:
            self.__model.usr_editable()
        elif "search" == p_flag:
            self.search()
        else:
            pass

    def search(self):
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        self.__model.usr_add(p_data)
